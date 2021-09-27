# taken from https://bcda.cms.gov/guide.html#try-the-api
# while the keys below are public, you should *never* commit your own id/secret to github

from bcda_client import ClientAuth

# 50 synthetic beneficiaries
EXTRA_SMALL_ACO = ClientAuth(
    "0c527d2e-2e8a-4808-b11d-0fa06baf8254",
    "36e0ea2217e6d6180f3ab1108d02ca100d684ebdccc04817ce842300996e568c3d77fc61d84006a3"
)

# 2,500 synthetic beneficiaries
SMALL_ACO = ClientAuth(
    "f0d89614-efb9-49fa-bb38-996811f235a1",
    "524a3e8985715d533ae4f182be3dd55778cc3b82179eb1b28759733fd5ddc787a535b548420af1a7"
)

# 7,500 synthetic beneficiaries
MEDIUM_ACO = ClientAuth(
    "635003cf-e337-4f91-be51-73b50e27ae9a",
    "5b1b45658dd9b75ef145a529c77d0c934e64788ba2ce9ce5195b834c1960a642aec689be485ad651"
)

# 20,000 synthetic beneficiaries
LARGE_ACO = ClientAuth(
    "8e85dd71-9206-44bb-a07e-638b29b316c1",
    "5104f03d92ccadf598bf75f5754acc923337361504a401b050cd4cf4e2dcd799c00bec361bf264ed"
)

# 30,000 synthetic beneficiaries
EXTRA_LARGE_ACO = ClientAuth(
    "aa2d6b93-bbe7-4d1b-8cc5-9a5172fae3a6",
    "3f18d01dbbc97634a10c0631c6cffced4d7949ddb2a54b6f400792fd55c5538473dbfccfe715bd8f"
)
