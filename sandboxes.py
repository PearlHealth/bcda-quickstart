# taken from https://bcda.cms.gov/guide.html#try-the-api
# while the keys below are public, you should *never* commit your own id/secret to github

from bcda_client import ClientAuth

# 50 synthetic beneficiaries
EXTRA_SMALL_ACO = ClientAuth(
    "3841c594-a8c0-41e5-98cc-38bb45360d3c",
    "d89810016460e6924a1c62583e5f51d1cbf911366c6bc6f040ff9f620a944efbf2b7264afe071609"
)

# 2,500 synthetic beneficiaries
SMALL_ACO = ClientAuth(
    "d5f83f74-6c55-4f1e-9d16-0022688171ba",
    "acc164b34eb88dd51dc2050ab1b9d7fc7b8781d21998201543ec288a2a85d9e6fbce64b11becb548"
)

# 7,500 synthetic beneficiaries
MEDIUM_ACO = ClientAuth(
    "8c75a6f6-02b9-4a47-96c1-0bd6efd4b5e3",
    "1f6a1cd9da34c0d0fe781d3e0d6b78c3ff9957f4796659ef2a1895a9f1f2d0cc01ee333db820aad4"
)

# 20,000 synthetic beneficiaries
LARGE_ACO = ClientAuth(
    "f268a8c6-8a29-4d2b-8b92-263dc775750d",
    "c8dc2fefa1f5eb3817df9ec8aaf6ec56f5a84f0eb085cc3fa2f495b7a2cdad77d31718a2c1ea8fce"
)

# 30,000 synthetic beneficiaries
EXTRA_LARGE_ACO = ClientAuth(
    "6152afb4-c555-46e4-93de-fa16a441d643",
    "9505e36662f6b59310360bc216d0b467c8f6f29c19dc8b40d91671ed4db7abb0fa2828c1524a595e"
)
