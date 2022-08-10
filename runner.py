import time
from datetime import datetime

import jsonlines
from fhir.resources.patient import Patient

from bcda_client import BCDAClient, ResourceType
from sandboxes import EXTRA_SMALL_ACO, SMALL_ADV_ACO, LARGE_ADV_ACO


def main():
    client = BCDAClient(EXTRA_SMALL_ACO)

    client.print_metadata()

    # types to request.
    # asking for less types makes the job take less time to complete.
    # resource types are
    #  - Patient (# as per the config selected)
    #  - Coverage (# x4 lines)
    #  - ExplanationOfBenefit (# x40 lines)
    resource_types = [ResourceType.Patient]

    # useful to get a delta from last check; the default time below gets us all data at the moment.
    # unfortunately, the synthetic data all has the exact same lastUpdated datetime, so can't play
    # around with it much. setting to now returns no records, as expected.
    since = datetime.fromisoformat("2021-06-01T08:00:00.000-05:00")
    print("Requesting files since " + str(since))

    client.run_patient_export_job(resource_types, since)

    print("Fetching job result")
    job_result = None
    i = 0
    while i != 720 and not job_result:
        job_result = client.fetch_job_result()
        time.sleep(3)
        i += 1

    if not job_result:
        client.cancel_current_job()
        raise Exception("Job taking longer than expected, check later")

    if job_result.is_error:
        print(str(job_result.error))
        raise Exception("Errors returned")

    if job_result.is_empty:
        print(f"Job returned no data (likely no data since {str(since)})")
        return

    output_files = job_result.output_map()
    print(f"Received URLs for the following resource types: " + ",".join(output_files.keys()))

    resource_type = ResourceType.Patient
    file_url = output_files[resource_type.value]
    stream = client.fetch_data_stream(resource_type, file_url)

    print(f"Loading records from stream")
    with jsonlines.Reader(stream) as reader:
        for obj in reader:
            first_patient = Patient(**obj)
            first_name = first_patient.name[0].given[0]
            last_name = first_patient.name[0].family
            last_updated = first_patient.meta.lastUpdated
            print(f"Found patient {first_name} {last_name} with id {first_patient.id}, last updated {last_updated}")


if __name__ == "__main__":
    main()
