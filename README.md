# Beneficiary Claims Data API (BCDA) v2 Quickstart

Implements a python starter client for the [CMS](https://www.cms.gov/) [BCDA](https://bcda.cms.gov/) API.
Makes it easy to get started after reading the following

- https://bcda.cms.gov/guide.html
- https://bcda.cms.gov/build.html

The API itself is served from [this project](https://github.com/CMSgov/bcda-app/blob/master/bcda/api/v2/api.go).

The bulk API returns [ndjson](http://ndjson.org/), and the json lines follow
the [FHIR](https://www.hl7.org/fhir/index.html) schema.

After some research I chose to use the following libraries for this proof of concept.

- https://github.com/wbolster/jsonlines
- https://github.com/nazrulworld/fhir.resources

### To use:

1. Pick one of the starter sandboxes with synthetic beneficiary data from `sandboxes.py`.
   The Extra Small ACO is passed in to the client by default in `runner.py`. Keep in mind that EOB data
   for Extra Small is 32MB, although Patient and Coverage files are much smaller. Choices are:

   * *Extra Small ACO - 50 beneficiaries*
   * *Small ACO - 2,500*
   * *Medium ACO - 7,500*
   * *Large ACO - 20,000*
   * *Extra Large ACO - 30,000*
   
2. Install dependencies. See requirements.txt.
   * `pip install -r bin/requirements.txt`

3. Before the first run, create the `out/` directory.
   * `mkdir out`

4. Run:
   * `python runner.py`
- Note: If you run into a FileNotFoundError, try creating the /out directory manually.

You will see something like this:

```
BCDA Server: https://sandbox.bcda.cms.gov
BCDA Release Version: r125
FHIR Version: 4.0.1
Requesting files since 2021-02-13 08:00:00-05:00
Fetching job result
Pending
Received URLs for the following resource types: Patient,Coverage
Downloading records of type Patient
Loading first record from file out/Patient-20210927123643.ndjson
Found patient Jane Doe with id -19990000000145, last updated 2021-06-07 21:50:48.169000-04:00
```

Negative IDs for patients means you are getting synthetic data from the sandbox environment.

You can take a look at downloaded patient files in the `out/` directory. In practice, these files
should be loaded to your data store before you access the [FHIR](https://www.hl7.org/fhir/patient.html)
entities and their elements.

The `since` parameter in the job calls can be used to get the delta from the last time we
fetched data. So, in practice, only the first fetch should be large i.e. download the whole db.
