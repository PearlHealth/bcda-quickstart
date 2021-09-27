import enum
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests
from fhir.resources.capabilitystatement import CapabilityStatement
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict

from bcda_client_responses import JobStatus


@dataclass
class ClientAuth:
    client_id: str = ""
    client_secret: str = ""


class ResourceType(enum.Enum):
    Patient = "Patient"
    Coverage = "Coverage"
    ExplanationOfBenefit = "ExplanationOfBenefit"


class BCDAClient:
    AUTH_TOKEN_PATH = "/auth/token"
    METADATA_PATH = "/api/v2/metadata"
    PATIENT_EXPORT_PATH = "/api/v2/Patient/$export"
    GROUP_EXPORT_PATH = "/api/v2/Group/all/$export"
    GROUP_RUNOUT_EXPORT_PATH = "/api/v2/Group/runout/$export"

    session: requests.Session = None
    dev_mode: bool = True
    current_job_url: str = ""

    def __init__(self, client_config: ClientAuth, dev_mode: bool = True):
        self.dev_mode = dev_mode
        self.__authenticate(client_config)

    def __endpoint_url(self, path: str):
        if self.dev_mode:
            return "https://sandbox.bcda.cms.gov" + path
        return "https://api.bcda.cms.gov" + path

    # Fetch a token and store a session. The token last 20 minutes.
    def __authenticate(self, client_config: ClientAuth):
        headers = CaseInsensitiveDict()
        headers["accept"] = "application/json"

        resp = requests.post(self.__endpoint_url(self.AUTH_TOKEN_PATH),
                             headers=headers,
                             auth=HTTPBasicAuth(
                                 client_config.client_id,
                                 client_config.client_secret
                             ))

        if resp.status_code != 200:
            raise Exception(f"code returned: {resp.status_code} error returned: {resp.text}")

        session = requests.Session()
        session.headers = {
            "Authorization": "Bearer " + resp.json()["access_token"]
        }

        self.session = session

    def print_metadata(self):
        headers = CaseInsensitiveDict()
        headers["accept"] = "application/json"

        resp = self.session.get(self.__endpoint_url(self.METADATA_PATH), headers=headers)

        if resp.status_code != 200:
            raise Exception(f"code returned: {resp.status_code} error returned: {resp.text}")

        metadata = CapabilityStatement.parse_raw(resp.content)
        print("BCDA Server: " + metadata.implementation.url)
        print("BCDA Release Version: " + metadata.software.version)
        print("FHIR Version: " + metadata.fhirVersion)

    @staticmethod
    def _get_params(resource_types: list[ResourceType] = [], since: datetime = None):
        payload = {}
        if len(resource_types) > 0:
            payload["_type"] = ",".join([x.value for x in resource_types])
        if since:
            payload["_since"] = since.isoformat()  # TODO perhaps bind to a fhir.resources.fhirtypes.Instant
        return payload

    # Run an async job to fetch bulk data. Returns the URL for checking job status.
    def _run_export_job(self, api_path: str, resource_types: list[ResourceType] = [], since: datetime = None):
        headers = CaseInsensitiveDict()
        headers["accept"] = "application/fhir+json"
        headers["Prefer"] = "respond-async"

        payload = self._get_params(resource_types, since)

        endpoint = self.__endpoint_url(api_path)
        resp = self.session.get(endpoint, headers=headers, params=payload)

        if resp.status_code != 202:
            raise Exception(f"code returned: {resp.status_code} error returned: {resp.text}")

        self.current_job_url = resp.headers["Content-Location"]

    def run_patient_export_job(self, resource_types: list[ResourceType] = [], since: datetime = None):
        self._run_export_job(self.PATIENT_EXPORT_PATH, resource_types, since)

    def run_group_export_job(self, resource_types: list[ResourceType] = [], since: datetime = None):
        self._run_export_job(self.GROUP_EXPORT_PATH, resource_types, since)

    def run_group_runout_export_job(self, resource_types: list[ResourceType] = [], since: datetime = None):
        self._run_export_job(self.GROUP_RUNOUT_EXPORT_PATH, resource_types, since)

    # For long-running jobs, cancel current job if needed
    def cancel_current_job(self):
        resp = self.session.delete(self.current_job_url)

        if resp.status_code != 202:
            raise Exception(f"code returned: {resp.status_code} error returned: {resp.text}")

    # Check on a job and print out status. If the job has completed, returns a JobStatus
    # with URLs to download Patient, Coverage, and EOB files.
    def fetch_job_result(self) -> Optional[JobStatus]:
        headers = CaseInsensitiveDict()
        headers["accept"] = "application/fhir+json"

        resp = self.session.get(self.current_job_url, headers=headers)

        if resp.status_code != 202 and resp.status_code != 200:
            raise Exception(f"code returned: {resp.status_code} error returned: {resp.text}")

        if resp.status_code == 202:
            print(resp.headers["X-Progress"])
        elif resp.status_code == 200:
            job_status = JobStatus.parse_raw(resp.content)
            return job_status

        return None

    # Download a file, return the path.
    # TODO stream rather than writing to disk.
    def fetch_data_file(self, record_type: ResourceType, file_url: str) -> str:
        headers = CaseInsensitiveDict()
        headers["Accept-Encoding"] = "gzip"

        print(f"Downloading records of type {record_type.value}")
        resp = self.session.get(file_url, headers=headers, stream=True)

        if resp.status_code != 200:
            raise Exception(f"code returned: {resp.status_code} error returned: {resp.text}")

        data_file_path = f'out/{record_type.value}-{time.strftime("%Y%m%d%H%M%S")}.ndjson'
        with open(data_file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024*512):
                f.write(chunk)

        return data_file_path
