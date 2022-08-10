# taken from https://bcda.cms.gov/guide.html#try-the-api
# while the keys below are public, you should *never* commit your own id/secret to github

from bcda_client import ClientAuth

# 50 synthetic beneficiaries
EXTRA_SMALL_ACO = ClientAuth(
    "3841c594-a8c0-41e5-98cc-38bb45360d3c",
    "d89810016460e6924a1c62583e5f51d1cbf911366c6bc6f040ff9f620a944efbf2b7264afe071609"
)

# 100 synthetic beneficiaries
SMALL_ADV_ACO = ClientAuth(
    "6dc59a4c-ef93-46c0-9c00-02e500e13731",
    "8d096fe469f61ab9148fa029eb0605065e069889bdbc8e465f0ee40a9edf59052a68f734794b6a6a"
)

# 10000 synthetic beneficiaries
LARGE_ADV_ACO = ClientAuth(
    "f5b6a686-0d7b-4080-873a-e60534fd2995",
    "02f8f1b7410c921682977ebfb8b82dcf57316a9ac4d5b20b5e9f8a3fc2ce8c57778b89301f2233f0"
)
