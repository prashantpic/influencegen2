# Specification

# 1. Entities

## 1.1. InfluencerProfile
Stores influencer profile information. Optimization Note: For 'audienceDemographics' (JSON type), if specific keys are frequently queried, use database-specific JSON indexing (e.g., GIN index in PostgreSQL for JSONB).

### 1.1.3. Attributes

### 1.1.3.1. id
#### 1.1.3.1.2. Type
UUID

#### 1.1.3.1.3. Is Required
True

#### 1.1.3.1.4. Is Primary Key
True

#### 1.1.3.1.5. Is Unique
True

#### 1.1.3.1.6. Default Value
gen_random_uuid()

### 1.1.3.2. fullName
#### 1.1.3.2.2. Type
VARCHAR

#### 1.1.3.2.3. Is Required
True

#### 1.1.3.2.4. Size
100

### 1.1.3.3. email
#### 1.1.3.3.2. Type
VARCHAR

#### 1.1.3.3.3. Is Required
True

#### 1.1.3.3.4. Is Unique
True

#### 1.1.3.3.5. Size
100

### 1.1.3.4. phone
#### 1.1.3.4.2. Type
VARCHAR

#### 1.1.3.4.3. Is Required
False

#### 1.1.3.4.4. Size
20

### 1.1.3.5. residentialAddress
#### 1.1.3.5.2. Type
VARCHAR

#### 1.1.3.5.3. Is Required
False

#### 1.1.3.5.4. Size
255

### 1.1.3.6. audienceDemographics
#### 1.1.3.6.2. Type
JSON

#### 1.1.3.6.3. Is Required
False

### 1.1.3.7. kycStatus
#### 1.1.3.7.2. Type
VARCHAR

#### 1.1.3.7.3. Is Required
True

#### 1.1.3.7.4. Size
20

#### 1.1.3.7.5. Default Value
'pending'

### 1.1.3.8. accountStatus
#### 1.1.3.8.2. Type
VARCHAR

#### 1.1.3.8.3. Is Required
True

#### 1.1.3.8.4. Size
20

#### 1.1.3.8.5. Default Value
'inactive'

### 1.1.3.9. createdAt
#### 1.1.3.9.2. Type
DateTime

#### 1.1.3.9.3. Is Required
True

#### 1.1.3.9.4. Default Value
CURRENT_TIMESTAMP

### 1.1.3.10. updatedAt
#### 1.1.3.10.2. Type
DateTime

#### 1.1.3.10.3. Is Required
True

#### 1.1.3.10.4. Default Value
CURRENT_TIMESTAMP


### 1.1.4. Primary Keys

- id

### 1.1.5. Unique Constraints

### 1.1.5.1. uq_influencerprofile_email
#### 1.1.5.1.2. Columns

- email


### 1.1.6. Indexes

### 1.1.6.1. idx_influencerprofile_kycstatus
#### 1.1.6.1.2. Columns

- kycStatus

#### 1.1.6.1.3. Type
BTree

### 1.1.6.2. idx_influencerprofile_accountstatus
#### 1.1.6.2.2. Columns

- accountStatus

#### 1.1.6.2.3. Type
BTree

### 1.1.6.3. idx_influencerprofile_createdat
#### 1.1.6.3.2. Columns

- createdAt

#### 1.1.6.3.3. Type
BTree

### 1.1.6.4. idx_influencerprofile_audemographics
#### 1.1.6.4.2. Columns

- audienceDemographics

#### 1.1.6.4.3. Type
GIN


## 1.2. AreaOfInfluence
Stores distinct areas of influence (Normalized from InfluencerProfile).

### 1.2.3. Attributes

### 1.2.3.1. id
#### 1.2.3.1.2. Type
UUID

#### 1.2.3.1.3. Is Required
True

#### 1.2.3.1.4. Is Primary Key
True

#### 1.2.3.1.5. Is Unique
True

#### 1.2.3.1.6. Default Value
gen_random_uuid()

### 1.2.3.2. name
#### 1.2.3.2.2. Type
VARCHAR

#### 1.2.3.2.3. Is Required
True

#### 1.2.3.2.4. Is Unique
True

#### 1.2.3.2.5. Size
100


### 1.2.4. Primary Keys

- id

### 1.2.5. Unique Constraints

### 1.2.5.1. uq_areaofinfluence_name
#### 1.2.5.1.2. Columns

- name


### 1.2.6. Indexes

### 1.2.6.1. idx_areaofinfluence_name
#### 1.2.6.1.2. Columns

- name

#### 1.2.6.1.3. Type
BTree


## 1.3. InfluencerAreaOfInfluence
Join table linking influencers to their areas of influence.

### 1.3.3. Attributes

### 1.3.3.1. influencerProfileId
#### 1.3.3.1.2. Type
UUID

#### 1.3.3.1.3. Is Required
True

#### 1.3.3.1.4. Is Primary Key
True

#### 1.3.3.1.5. Is Foreign Key
True

#### 1.3.3.1.6. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.3.3.2. areaOfInfluenceId
#### 1.3.3.2.2. Type
UUID

#### 1.3.3.2.3. Is Required
True

#### 1.3.3.2.4. Is Primary Key
True

#### 1.3.3.2.5. Is Foreign Key
True

#### 1.3.3.2.6. Constraints

- REFERENCES AreaOfInfluence(id) ON DELETE CASCADE


### 1.3.4. Primary Keys

- influencerProfileId
- areaOfInfluenceId

### 1.3.5. Unique Constraints


### 1.3.6. Indexes

### 1.3.6.1. idx_influencerarea_areaid
#### 1.3.6.1.2. Columns

- areaOfInfluenceId

#### 1.3.6.1.3. Type
BTree


## 1.4. SocialMediaProfile
Stores influencer social media accounts

### 1.4.3. Attributes

### 1.4.3.1. id
#### 1.4.3.1.2. Type
UUID

#### 1.4.3.1.3. Is Required
True

#### 1.4.3.1.4. Is Primary Key
True

#### 1.4.3.1.5. Is Unique
True

#### 1.4.3.1.6. Default Value
gen_random_uuid()

### 1.4.3.2. influencerProfileId
#### 1.4.3.2.2. Type
UUID

#### 1.4.3.2.3. Is Required
True

#### 1.4.3.2.4. Is Foreign Key
True

#### 1.4.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.4.3.3. platform
#### 1.4.3.3.2. Type
VARCHAR

#### 1.4.3.3.3. Is Required
True

#### 1.4.3.3.4. Size
50

### 1.4.3.4. handle
#### 1.4.3.4.2. Type
VARCHAR

#### 1.4.3.4.3. Is Required
True

#### 1.4.3.4.4. Size
100

### 1.4.3.5. verificationStatus
#### 1.4.3.5.2. Type
VARCHAR

#### 1.4.3.5.3. Is Required
True

#### 1.4.3.5.4. Size
20

#### 1.4.3.5.5. Default Value
'pending'

### 1.4.3.6. verificationMethod
#### 1.4.3.6.2. Type
VARCHAR

#### 1.4.3.6.3. Is Required
False

#### 1.4.3.6.4. Size
50

### 1.4.3.7. verificationCode
#### 1.4.3.7.2. Type
VARCHAR

#### 1.4.3.7.3. Is Required
False

#### 1.4.3.7.4. Size
50

### 1.4.3.8. verifiedAt
#### 1.4.3.8.2. Type
DateTime

#### 1.4.3.8.3. Is Required
False

### 1.4.3.9. createdAt
#### 1.4.3.9.2. Type
DateTime

#### 1.4.3.9.3. Is Required
True

#### 1.4.3.9.4. Default Value
CURRENT_TIMESTAMP

### 1.4.3.10. updatedAt
#### 1.4.3.10.2. Type
DateTime

#### 1.4.3.10.3. Is Required
True

#### 1.4.3.10.4. Default Value
CURRENT_TIMESTAMP


### 1.4.4. Primary Keys

- id

### 1.4.5. Unique Constraints

### 1.4.5.1. uq_socialmediaprofile_platform_handle
#### 1.4.5.1.2. Columns

- platform
- handle


### 1.4.6. Indexes

### 1.4.6.1. idx_socialmediaprofile_influencerid
#### 1.4.6.1.2. Columns

- influencerProfileId

#### 1.4.6.1.3. Type
BTree


## 1.5. KYCData
Stores KYC verification information

### 1.5.3. Attributes

### 1.5.3.1. id
#### 1.5.3.1.2. Type
UUID

#### 1.5.3.1.3. Is Required
True

#### 1.5.3.1.4. Is Primary Key
True

#### 1.5.3.1.5. Is Unique
True

#### 1.5.3.1.6. Default Value
gen_random_uuid()

### 1.5.3.2. influencerProfileId
#### 1.5.3.2.2. Type
UUID

#### 1.5.3.2.3. Is Required
True

#### 1.5.3.2.4. Is Foreign Key
True

#### 1.5.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.5.3.3. documentType
#### 1.5.3.3.2. Type
VARCHAR

#### 1.5.3.3.3. Is Required
True

#### 1.5.3.3.4. Size
50

### 1.5.3.4. documentFrontUrl
#### 1.5.3.4.2. Type
VARCHAR

#### 1.5.3.4.3. Is Required
True

#### 1.5.3.4.4. Size
255

### 1.5.3.5. documentBackUrl
#### 1.5.3.5.2. Type
VARCHAR

#### 1.5.3.5.3. Is Required
False

#### 1.5.3.5.4. Size
255

### 1.5.3.6. verificationMethod
#### 1.5.3.6.2. Type
VARCHAR

#### 1.5.3.6.3. Is Required
True

#### 1.5.3.6.4. Size
50

### 1.5.3.7. verificationStatus
#### 1.5.3.7.2. Type
VARCHAR

#### 1.5.3.7.3. Is Required
True

#### 1.5.3.7.4. Size
20

#### 1.5.3.7.5. Default Value
'pending'

### 1.5.3.8. reviewerId
#### 1.5.3.8.2. Type
UUID

#### 1.5.3.8.3. Is Required
False

#### 1.5.3.8.4. Is Foreign Key
True

#### 1.5.3.8.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE SET NULL

### 1.5.3.9. reviewedAt
#### 1.5.3.9.2. Type
DateTime

#### 1.5.3.9.3. Is Required
False

### 1.5.3.10. notes
#### 1.5.3.10.2. Type
TEXT

#### 1.5.3.10.3. Is Required
False

### 1.5.3.11. createdAt
#### 1.5.3.11.2. Type
DateTime

#### 1.5.3.11.3. Is Required
True

#### 1.5.3.11.4. Default Value
CURRENT_TIMESTAMP

### 1.5.3.12. updatedAt
#### 1.5.3.12.2. Type
DateTime

#### 1.5.3.12.3. Is Required
True

#### 1.5.3.12.4. Default Value
CURRENT_TIMESTAMP


### 1.5.4. Primary Keys

- id

### 1.5.5. Unique Constraints


### 1.5.6. Indexes

### 1.5.6.1. idx_kycdata_influencerid
#### 1.5.6.1.2. Columns

- influencerProfileId

#### 1.5.6.1.3. Type
BTree

### 1.5.6.2. idx_kycdata_verificationstatus
#### 1.5.6.2.2. Columns

- verificationStatus

#### 1.5.6.2.3. Type
BTree


## 1.6. BankAccount
Stores influencer bank account details

### 1.6.3. Attributes

### 1.6.3.1. id
#### 1.6.3.1.2. Type
UUID

#### 1.6.3.1.3. Is Required
True

#### 1.6.3.1.4. Is Primary Key
True

#### 1.6.3.1.5. Is Unique
True

#### 1.6.3.1.6. Default Value
gen_random_uuid()

### 1.6.3.2. influencerProfileId
#### 1.6.3.2.2. Type
UUID

#### 1.6.3.2.3. Is Required
True

#### 1.6.3.2.4. Is Foreign Key
True

#### 1.6.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.6.3.3. accountHolderName
#### 1.6.3.3.2. Type
VARCHAR

#### 1.6.3.3.3. Is Required
True

#### 1.6.3.3.4. Size
100

### 1.6.3.4. accountNumber
#### 1.6.3.4.2. Type
VARCHAR

#### 1.6.3.4.3. Is Required
True

#### 1.6.3.4.4. Size
50

### 1.6.3.5. bankName
#### 1.6.3.5.2. Type
VARCHAR

#### 1.6.3.5.3. Is Required
True

#### 1.6.3.5.4. Size
100

### 1.6.3.6. routingNumber
#### 1.6.3.6.2. Type
VARCHAR

#### 1.6.3.6.3. Is Required
False

#### 1.6.3.6.4. Size
30

### 1.6.3.7. iban
#### 1.6.3.7.2. Type
VARCHAR

#### 1.6.3.7.3. Is Required
False

#### 1.6.3.7.4. Size
34

### 1.6.3.8. swiftCode
#### 1.6.3.8.2. Type
VARCHAR

#### 1.6.3.8.3. Is Required
False

#### 1.6.3.8.4. Size
11

### 1.6.3.9. verificationStatus
#### 1.6.3.9.2. Type
VARCHAR

#### 1.6.3.9.3. Is Required
True

#### 1.6.3.9.4. Size
20

#### 1.6.3.9.5. Default Value
'pending'

### 1.6.3.10. verificationMethod
#### 1.6.3.10.2. Type
VARCHAR

#### 1.6.3.10.3. Is Required
False

#### 1.6.3.10.4. Size
50

### 1.6.3.11. isPrimary
#### 1.6.3.11.2. Type
BOOLEAN

#### 1.6.3.11.3. Is Required
True

#### 1.6.3.11.4. Default Value
false

### 1.6.3.12. createdAt
#### 1.6.3.12.2. Type
DateTime

#### 1.6.3.12.3. Is Required
True

#### 1.6.3.12.4. Default Value
CURRENT_TIMESTAMP

### 1.6.3.13. updatedAt
#### 1.6.3.13.2. Type
DateTime

#### 1.6.3.13.3. Is Required
True

#### 1.6.3.13.4. Default Value
CURRENT_TIMESTAMP


### 1.6.4. Primary Keys

- id

### 1.6.5. Unique Constraints


### 1.6.6. Indexes

### 1.6.6.1. idx_bankaccount_influencerid
#### 1.6.6.1.2. Columns

- influencerProfileId

#### 1.6.6.1.3. Type
BTree

### 1.6.6.2. idx_bankaccount_influencer_isprimary
#### 1.6.6.2.2. Columns

- influencerProfileId
- isPrimary

#### 1.6.6.2.3. Type
BTree


## 1.7. Campaign
Stores marketing campaign details. Optimization Note: Cache details of 'Published/Open' campaigns (where status = 'Published/Open') as these are frequently browsed by influencers. For 'targetCriteria' (JSON type), if specific keys are frequently used for filtering, use database-specific JSON indexing. Use read replicas for serving campaign browsing.

### 1.7.3. Attributes

### 1.7.3.1. id
#### 1.7.3.1.2. Type
UUID

#### 1.7.3.1.3. Is Required
True

#### 1.7.3.1.4. Is Primary Key
True

#### 1.7.3.1.5. Is Unique
True

#### 1.7.3.1.6. Default Value
gen_random_uuid()

### 1.7.3.2. name
#### 1.7.3.2.2. Type
VARCHAR

#### 1.7.3.2.3. Is Required
True

#### 1.7.3.2.4. Is Unique
True

#### 1.7.3.2.5. Size
100

#### 1.7.3.2.6. Index Type
FullText

### 1.7.3.3. description
#### 1.7.3.3.2. Type
TEXT

#### 1.7.3.3.3. Is Required
True

#### 1.7.3.3.4. Index Type
FullText

### 1.7.3.4. brandClient
#### 1.7.3.4.2. Type
VARCHAR

#### 1.7.3.4.3. Is Required
True

#### 1.7.3.4.4. Size
100

### 1.7.3.5. goals
#### 1.7.3.5.2. Type
TEXT

#### 1.7.3.5.3. Is Required
True

### 1.7.3.6. targetCriteria
#### 1.7.3.6.2. Type
JSON

#### 1.7.3.6.3. Is Required
True

### 1.7.3.7. contentRequirements
#### 1.7.3.7.2. Type
TEXT

#### 1.7.3.7.3. Is Required
True

#### 1.7.3.7.4. Index Type
FullText

### 1.7.3.8. budget
#### 1.7.3.8.2. Type
DECIMAL

#### 1.7.3.8.3. Is Required
False

#### 1.7.3.8.4. Precision
15

#### 1.7.3.8.5. Scale
2

### 1.7.3.9. compensationModel
#### 1.7.3.9.2. Type
VARCHAR

#### 1.7.3.9.3. Is Required
True

#### 1.7.3.9.4. Size
50

### 1.7.3.10. submissionDeadline
#### 1.7.3.10.2. Type
DateTime

#### 1.7.3.10.3. Is Required
True

### 1.7.3.11. startDate
#### 1.7.3.11.2. Type
DateTime

#### 1.7.3.11.3. Is Required
True

### 1.7.3.12. endDate
#### 1.7.3.12.2. Type
DateTime

#### 1.7.3.12.3. Is Required
True

### 1.7.3.13. usageRights
#### 1.7.3.13.2. Type
TEXT

#### 1.7.3.13.3. Is Required
True

### 1.7.3.14. status
#### 1.7.3.14.2. Type
VARCHAR

#### 1.7.3.14.3. Is Required
True

#### 1.7.3.14.4. Size
20

#### 1.7.3.14.5. Default Value
'draft'

### 1.7.3.15. createdAt
#### 1.7.3.15.2. Type
DateTime

#### 1.7.3.15.3. Is Required
True

#### 1.7.3.15.4. Default Value
CURRENT_TIMESTAMP

### 1.7.3.16. updatedAt
#### 1.7.3.16.2. Type
DateTime

#### 1.7.3.16.3. Is Required
True

#### 1.7.3.16.4. Default Value
CURRENT_TIMESTAMP


### 1.7.4. Primary Keys

- id

### 1.7.5. Unique Constraints

### 1.7.5.1. uq_campaign_name
#### 1.7.5.1.2. Columns

- name


### 1.7.6. Indexes

### 1.7.6.1. idx_campaign_status
#### 1.7.6.1.2. Columns

- status

#### 1.7.6.1.3. Type
BTree

### 1.7.6.2. idx_campaign_submissiondeadline
#### 1.7.6.2.2. Columns

- submissionDeadline

#### 1.7.6.2.3. Type
BTree

### 1.7.6.3. idx_campaign_startdate
#### 1.7.6.3.2. Columns

- startDate

#### 1.7.6.3.3. Type
BTree

### 1.7.6.4. idx_campaign_enddate
#### 1.7.6.4.2. Columns

- endDate

#### 1.7.6.4.3. Type
BTree

### 1.7.6.5. idx_campaign_compensationmodel
#### 1.7.6.5.2. Columns

- compensationModel

#### 1.7.6.5.3. Type
BTree

### 1.7.6.6. idx_campaign_targetcriteria
#### 1.7.6.6.2. Columns

- targetCriteria

#### 1.7.6.6.3. Type
GIN


## 1.8. CampaignApplication
Stores influencer applications to campaigns

### 1.8.3. Attributes

### 1.8.3.1. id
#### 1.8.3.1.2. Type
UUID

#### 1.8.3.1.3. Is Required
True

#### 1.8.3.1.4. Is Primary Key
True

#### 1.8.3.1.5. Is Unique
True

#### 1.8.3.1.6. Default Value
gen_random_uuid()

### 1.8.3.2. campaignId
#### 1.8.3.2.2. Type
UUID

#### 1.8.3.2.3. Is Required
True

#### 1.8.3.2.4. Is Foreign Key
True

#### 1.8.3.2.5. Constraints

- REFERENCES Campaign(id) ON DELETE CASCADE

### 1.8.3.3. influencerProfileId
#### 1.8.3.3.2. Type
UUID

#### 1.8.3.3.3. Is Required
True

#### 1.8.3.3.4. Is Foreign Key
True

#### 1.8.3.3.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.8.3.4. proposal
#### 1.8.3.4.2. Type
TEXT

#### 1.8.3.4.3. Is Required
False

### 1.8.3.5. status
#### 1.8.3.5.2. Type
VARCHAR

#### 1.8.3.5.3. Is Required
True

#### 1.8.3.5.4. Size
20

#### 1.8.3.5.5. Default Value
'submitted'

### 1.8.3.6. submittedAt
#### 1.8.3.6.2. Type
DateTime

#### 1.8.3.6.3. Is Required
True

#### 1.8.3.6.4. Default Value
CURRENT_TIMESTAMP

### 1.8.3.7. reviewedAt
#### 1.8.3.7.2. Type
DateTime

#### 1.8.3.7.3. Is Required
False

### 1.8.3.8. reviewerId
#### 1.8.3.8.2. Type
UUID

#### 1.8.3.8.3. Is Required
False

#### 1.8.3.8.4. Is Foreign Key
True

#### 1.8.3.8.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE SET NULL

### 1.8.3.9. rejectionReason
#### 1.8.3.9.2. Type
TEXT

#### 1.8.3.9.3. Is Required
False


### 1.8.4. Primary Keys

- id

### 1.8.5. Unique Constraints

### 1.8.5.1. uq_campaignapplication_campaign_influencer
#### 1.8.5.1.2. Columns

- campaignId
- influencerProfileId


### 1.8.6. Indexes

### 1.8.6.1. idx_campaignapplication_campaign_status
#### 1.8.6.1.2. Columns

- campaignId
- status

#### 1.8.6.1.3. Type
BTree

### 1.8.6.2. idx_campaignapplication_influencer_status
#### 1.8.6.2.2. Columns

- influencerProfileId
- status

#### 1.8.6.2.3. Type
BTree


## 1.9. ContentSubmission
Stores content submitted by influencers. Optimization Note: Consider range partitioning by 'submissionDate' if the table is expected to grow very large.

### 1.9.3. Attributes

### 1.9.3.1. id
#### 1.9.3.1.2. Type
UUID

#### 1.9.3.1.3. Is Required
True

#### 1.9.3.1.4. Is Primary Key
True

#### 1.9.3.1.5. Is Unique
True

#### 1.9.3.1.6. Default Value
gen_random_uuid()

### 1.9.3.2. campaignApplicationId
#### 1.9.3.2.2. Type
UUID

#### 1.9.3.2.3. Is Required
True

#### 1.9.3.2.4. Is Foreign Key
True

#### 1.9.3.2.5. Constraints

- REFERENCES CampaignApplication(id) ON DELETE CASCADE

### 1.9.3.3. contentUrl
#### 1.9.3.3.2. Type
VARCHAR

#### 1.9.3.3.3. Is Required
True

#### 1.9.3.3.4. Size
255

### 1.9.3.4. fileType
#### 1.9.3.4.2. Type
VARCHAR

#### 1.9.3.4.3. Is Required
True

#### 1.9.3.4.4. Size
10

### 1.9.3.5. fileSize
#### 1.9.3.5.2. Type
INT

#### 1.9.3.5.3. Is Required
True

### 1.9.3.6. submissionDate
#### 1.9.3.6.2. Type
DateTime

#### 1.9.3.6.3. Is Required
True

#### 1.9.3.6.4. Default Value
CURRENT_TIMESTAMP

### 1.9.3.7. reviewStatus
#### 1.9.3.7.2. Type
VARCHAR

#### 1.9.3.7.3. Is Required
True

#### 1.9.3.7.4. Size
20

#### 1.9.3.7.5. Default Value
'pending'

### 1.9.3.8. feedback
#### 1.9.3.8.2. Type
TEXT

#### 1.9.3.8.3. Is Required
False

### 1.9.3.9. reviewedById
#### 1.9.3.9.2. Type
UUID

#### 1.9.3.9.3. Is Required
False

#### 1.9.3.9.4. Is Foreign Key
True

#### 1.9.3.9.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE SET NULL

### 1.9.3.10. reviewedAt
#### 1.9.3.10.2. Type
DateTime

#### 1.9.3.10.3. Is Required
False

### 1.9.3.11. version
#### 1.9.3.11.2. Type
INT

#### 1.9.3.11.3. Is Required
True

#### 1.9.3.11.4. Default Value
1


### 1.9.4. Primary Keys

- id

### 1.9.5. Unique Constraints


### 1.9.6. Indexes

### 1.9.6.1. idx_contentsubmission_campaignapplicationid
#### 1.9.6.1.2. Columns

- campaignApplicationId

#### 1.9.6.1.3. Type
BTree

### 1.9.6.2. idx_contentsubmission_reviewstatus
#### 1.9.6.2.2. Columns

- reviewStatus

#### 1.9.6.2.3. Type
BTree


## 1.10. AIImageModel
Stores available AI image generation models. Optimization Note: Cache frequently accessed, rarely changing data like active AIImageModel details (where isActive = true).

### 1.10.3. Attributes

### 1.10.3.1. id
#### 1.10.3.1.2. Type
UUID

#### 1.10.3.1.3. Is Required
True

#### 1.10.3.1.4. Is Primary Key
True

#### 1.10.3.1.5. Is Unique
True

#### 1.10.3.1.6. Default Value
gen_random_uuid()

### 1.10.3.2. name
#### 1.10.3.2.2. Type
VARCHAR

#### 1.10.3.2.3. Is Required
True

#### 1.10.3.2.4. Is Unique
True

#### 1.10.3.2.5. Size
50

### 1.10.3.3. description
#### 1.10.3.3.2. Type
TEXT

#### 1.10.3.3.3. Is Required
False

### 1.10.3.4. triggerKeywords
#### 1.10.3.4.2. Type
VARCHAR

#### 1.10.3.4.3. Is Required
False

#### 1.10.3.4.4. Size
255

### 1.10.3.5. isActive
#### 1.10.3.5.2. Type
BOOLEAN

#### 1.10.3.5.3. Is Required
True

#### 1.10.3.5.4. Default Value
true

### 1.10.3.6. createdAt
#### 1.10.3.6.2. Type
DateTime

#### 1.10.3.6.3. Is Required
True

#### 1.10.3.6.4. Default Value
CURRENT_TIMESTAMP

### 1.10.3.7. updatedAt
#### 1.10.3.7.2. Type
DateTime

#### 1.10.3.7.3. Is Required
True

#### 1.10.3.7.4. Default Value
CURRENT_TIMESTAMP


### 1.10.4. Primary Keys

- id

### 1.10.5. Unique Constraints

### 1.10.5.1. uq_aiimagemodel_name
#### 1.10.5.1.2. Columns

- name


### 1.10.6. Indexes

### 1.10.6.1. idx_aiimagemodel_isactive
#### 1.10.6.1.2. Columns

- isActive

#### 1.10.6.1.3. Type
BTree


## 1.11. AIImageGenerationRequest
Stores AI image generation requests

### 1.11.3. Attributes

### 1.11.3.1. id
#### 1.11.3.1.2. Type
UUID

#### 1.11.3.1.3. Is Required
True

#### 1.11.3.1.4. Is Primary Key
True

#### 1.11.3.1.5. Is Unique
True

#### 1.11.3.1.6. Default Value
gen_random_uuid()

### 1.11.3.2. userId
#### 1.11.3.2.2. Type
UUID

#### 1.11.3.2.3. Is Required
True

#### 1.11.3.2.4. Is Foreign Key
True

#### 1.11.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.11.3.3. campaignId
#### 1.11.3.3.2. Type
UUID

#### 1.11.3.3.3. Is Required
False

#### 1.11.3.3.4. Is Foreign Key
True

#### 1.11.3.3.5. Constraints

- REFERENCES Campaign(id) ON DELETE SET NULL

### 1.11.3.4. prompt
#### 1.11.3.4.2. Type
TEXT

#### 1.11.3.4.3. Is Required
True

### 1.11.3.5. negativePrompt
#### 1.11.3.5.2. Type
TEXT

#### 1.11.3.5.3. Is Required
False

### 1.11.3.6. modelId
#### 1.11.3.6.2. Type
UUID

#### 1.11.3.6.3. Is Required
True

#### 1.11.3.6.4. Is Foreign Key
True

#### 1.11.3.6.5. Constraints

- REFERENCES AIImageModel(id) ON DELETE RESTRICT

### 1.11.3.7. resolution
#### 1.11.3.7.2. Type
VARCHAR

#### 1.11.3.7.3. Is Required
True

#### 1.11.3.7.4. Size
20

### 1.11.3.8. aspectRatio
#### 1.11.3.8.2. Type
VARCHAR

#### 1.11.3.8.3. Is Required
True

#### 1.11.3.8.4. Size
10

### 1.11.3.9. seed
#### 1.11.3.9.2. Type
INT

#### 1.11.3.9.3. Is Required
False

### 1.11.3.10. inferenceSteps
#### 1.11.3.10.2. Type
INT

#### 1.11.3.10.3. Is Required
False

### 1.11.3.11. cfgScale
#### 1.11.3.11.2. Type
DECIMAL

#### 1.11.3.11.3. Is Required
False

#### 1.11.3.11.4. Precision
3

#### 1.11.3.11.5. Scale
1

### 1.11.3.12. status
#### 1.11.3.12.2. Type
VARCHAR

#### 1.11.3.12.3. Is Required
True

#### 1.11.3.12.4. Size
20

#### 1.11.3.12.5. Default Value
'queued'

### 1.11.3.13. errorDetails
#### 1.11.3.13.2. Type
TEXT

#### 1.11.3.13.3. Is Required
False

### 1.11.3.14. createdAt
#### 1.11.3.14.2. Type
DateTime

#### 1.11.3.14.3. Is Required
True

#### 1.11.3.14.4. Default Value
CURRENT_TIMESTAMP

### 1.11.3.15. updatedAt
#### 1.11.3.15.2. Type
DateTime

#### 1.11.3.15.3. Is Required
True

#### 1.11.3.15.4. Default Value
CURRENT_TIMESTAMP


### 1.11.4. Primary Keys

- id

### 1.11.5. Unique Constraints


### 1.11.6. Indexes

### 1.11.6.1. idx_aiimagerequest_userid
#### 1.11.6.1.2. Columns

- userId

#### 1.11.6.1.3. Type
BTree

### 1.11.6.2. idx_aiimagerequest_status
#### 1.11.6.2.2. Columns

- status

#### 1.11.6.2.3. Type
BTree


## 1.12. GeneratedImage
Stores generated AI images metadata. Optimization Note: If table becomes extremely large, consider partitioning by 'createdAt'.

### 1.12.3. Attributes

### 1.12.3.1. id
#### 1.12.3.1.2. Type
UUID

#### 1.12.3.1.3. Is Required
True

#### 1.12.3.1.4. Is Primary Key
True

#### 1.12.3.1.5. Is Unique
True

#### 1.12.3.1.6. Default Value
gen_random_uuid()

### 1.12.3.2. requestId
#### 1.12.3.2.2. Type
UUID

#### 1.12.3.2.3. Is Required
True

#### 1.12.3.2.4. Is Foreign Key
True

#### 1.12.3.2.5. Constraints

- REFERENCES AIImageGenerationRequest(id) ON DELETE CASCADE

### 1.12.3.3. storageUrl
#### 1.12.3.3.2. Type
VARCHAR

#### 1.12.3.3.3. Is Required
True

#### 1.12.3.3.4. Size
255

### 1.12.3.4. fileFormat
#### 1.12.3.4.2. Type
VARCHAR

#### 1.12.3.4.3. Is Required
True

#### 1.12.3.4.4. Size
10

### 1.12.3.5. fileSize
#### 1.12.3.5.2. Type
INT

#### 1.12.3.5.3. Is Required
True

### 1.12.3.6. width
#### 1.12.3.6.2. Type
INT

#### 1.12.3.6.3. Is Required
True

### 1.12.3.7. height
#### 1.12.3.7.2. Type
INT

#### 1.12.3.7.3. Is Required
True

### 1.12.3.8. hashValue
#### 1.12.3.8.2. Type
VARCHAR

#### 1.12.3.8.3. Is Required
True

#### 1.12.3.8.4. Size
64

### 1.12.3.9. retentionCategory
#### 1.12.3.9.2. Type
VARCHAR

#### 1.12.3.9.3. Is Required
True

#### 1.12.3.9.4. Size
30

### 1.12.3.10. usageRights
#### 1.12.3.10.2. Type
TEXT

#### 1.12.3.10.3. Is Required
False

### 1.12.3.11. createdAt
#### 1.12.3.11.2. Type
DateTime

#### 1.12.3.11.3. Is Required
True

#### 1.12.3.11.4. Default Value
CURRENT_TIMESTAMP


### 1.12.4. Primary Keys

- id

### 1.12.5. Unique Constraints


### 1.12.6. Indexes

### 1.12.6.1. idx_generatedimage_requestid
#### 1.12.6.1.2. Columns

- requestId

#### 1.12.6.1.3. Type
BTree

### 1.12.6.2. idx_generatedimage_hashvalue
#### 1.12.6.2.2. Columns

- hashValue

#### 1.12.6.2.3. Type
BTree


## 1.13. PaymentRecord
Stores influencer payment records

### 1.13.3. Attributes

### 1.13.3.1. id
#### 1.13.3.1.2. Type
UUID

#### 1.13.3.1.3. Is Required
True

#### 1.13.3.1.4. Is Primary Key
True

#### 1.13.3.1.5. Is Unique
True

#### 1.13.3.1.6. Default Value
gen_random_uuid()

### 1.13.3.2. influencerProfileId
#### 1.13.3.2.2. Type
UUID

#### 1.13.3.2.3. Is Required
True

#### 1.13.3.2.4. Is Foreign Key
True

#### 1.13.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE RESTRICT

### 1.13.3.3. campaignId
#### 1.13.3.3.2. Type
UUID

#### 1.13.3.3.3. Is Required
False

#### 1.13.3.3.4. Is Foreign Key
True

#### 1.13.3.3.5. Constraints

- REFERENCES Campaign(id) ON DELETE SET NULL

### 1.13.3.4. amount
#### 1.13.3.4.2. Type
DECIMAL

#### 1.13.3.4.3. Is Required
True

#### 1.13.3.4.4. Precision
15

#### 1.13.3.4.5. Scale
2

### 1.13.3.5. currency
#### 1.13.3.5.2. Type
VARCHAR

#### 1.13.3.5.3. Is Required
True

#### 1.13.3.5.4. Size
3

### 1.13.3.6. status
#### 1.13.3.6.2. Type
VARCHAR

#### 1.13.3.6.3. Is Required
True

#### 1.13.3.6.4. Size
20

#### 1.13.3.6.5. Default Value
'pending'

### 1.13.3.7. transactionId
#### 1.13.3.7.2. Type
VARCHAR

#### 1.13.3.7.3. Is Required
False

#### 1.13.3.7.4. Size
50

### 1.13.3.8. paymentMethod
#### 1.13.3.8.2. Type
VARCHAR

#### 1.13.3.8.3. Is Required
True

#### 1.13.3.8.4. Size
50

### 1.13.3.9. dueDate
#### 1.13.3.9.2. Type
DateTime

#### 1.13.3.9.3. Is Required
False

### 1.13.3.10. paidDate
#### 1.13.3.10.2. Type
DateTime

#### 1.13.3.10.3. Is Required
False

### 1.13.3.11. createdAt
#### 1.13.3.11.2. Type
DateTime

#### 1.13.3.11.3. Is Required
True

#### 1.13.3.11.4. Default Value
CURRENT_TIMESTAMP

### 1.13.3.12. updatedAt
#### 1.13.3.12.2. Type
DateTime

#### 1.13.3.12.3. Is Required
True

#### 1.13.3.12.4. Default Value
CURRENT_TIMESTAMP


### 1.13.4. Primary Keys

- id

### 1.13.5. Unique Constraints


### 1.13.6. Indexes

### 1.13.6.1. idx_paymentrecord_influencer_status
#### 1.13.6.1.2. Columns

- influencerProfileId
- status

#### 1.13.6.1.3. Type
BTree

### 1.13.6.2. idx_paymentrecord_status
#### 1.13.6.2.2. Columns

- status

#### 1.13.6.2.3. Type
BTree


## 1.14. TermsConsent
Stores terms of service consent records

### 1.14.3. Attributes

### 1.14.3.1. id
#### 1.14.3.1.2. Type
UUID

#### 1.14.3.1.3. Is Required
True

#### 1.14.3.1.4. Is Primary Key
True

#### 1.14.3.1.5. Is Unique
True

#### 1.14.3.1.6. Default Value
gen_random_uuid()

### 1.14.3.2. influencerProfileId
#### 1.14.3.2.2. Type
UUID

#### 1.14.3.2.3. Is Required
True

#### 1.14.3.2.4. Is Foreign Key
True

#### 1.14.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.14.3.3. tosVersion
#### 1.14.3.3.2. Type
VARCHAR

#### 1.14.3.3.3. Is Required
True

#### 1.14.3.3.4. Size
20

### 1.14.3.4. privacyPolicyVersion
#### 1.14.3.4.2. Type
VARCHAR

#### 1.14.3.4.3. Is Required
True

#### 1.14.3.4.4. Size
20

### 1.14.3.5. consentDate
#### 1.14.3.5.2. Type
DateTime

#### 1.14.3.5.3. Is Required
True

#### 1.14.3.5.4. Default Value
CURRENT_TIMESTAMP

### 1.14.3.6. createdAt
#### 1.14.3.6.2. Type
DateTime

#### 1.14.3.6.3. Is Required
True

#### 1.14.3.6.4. Default Value
CURRENT_TIMESTAMP


### 1.14.4. Primary Keys

- id

### 1.14.5. Unique Constraints


### 1.14.6. Indexes

### 1.14.6.1. idx_termsconsent_influencer_consentdate
#### 1.14.6.1.2. Columns

- influencerProfileId
- consentDate DESC

#### 1.14.6.1.3. Type
BTree


## 1.15. AuditLog
Stores system audit trail records. Optimization Note: Implement range partitioning on this table using the 'timestamp' column (e.g., monthly or quarterly partitions).

### 1.15.3. Attributes

### 1.15.3.1. id
#### 1.15.3.1.2. Type
UUID

#### 1.15.3.1.3. Is Required
True

#### 1.15.3.1.4. Is Primary Key
True

#### 1.15.3.1.5. Is Unique
True

#### 1.15.3.1.6. Default Value
gen_random_uuid()

### 1.15.3.2. eventType
#### 1.15.3.2.2. Type
VARCHAR

#### 1.15.3.2.3. Is Required
True

#### 1.15.3.2.4. Size
50

### 1.15.3.3. userId
#### 1.15.3.3.2. Type
UUID

#### 1.15.3.3.3. Is Required
False

#### 1.15.3.3.4. Is Foreign Key
True

#### 1.15.3.3.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE SET NULL

### 1.15.3.4. targetEntity
#### 1.15.3.4.2. Type
VARCHAR

#### 1.15.3.4.3. Is Required
True

#### 1.15.3.4.4. Size
50

### 1.15.3.5. targetId
#### 1.15.3.5.2. Type
UUID

#### 1.15.3.5.3. Is Required
False

### 1.15.3.6. action
#### 1.15.3.6.2. Type
VARCHAR

#### 1.15.3.6.3. Is Required
True

#### 1.15.3.6.4. Size
20

### 1.15.3.7. details
#### 1.15.3.7.2. Type
JSON

#### 1.15.3.7.3. Is Required
False

### 1.15.3.8. ipAddress
#### 1.15.3.8.2. Type
VARCHAR

#### 1.15.3.8.3. Is Required
False

#### 1.15.3.8.4. Size
45

### 1.15.3.9. timestamp
#### 1.15.3.9.2. Type
DateTime

#### 1.15.3.9.3. Is Required
True

#### 1.15.3.9.4. Default Value
CURRENT_TIMESTAMP


### 1.15.4. Primary Keys

- id

### 1.15.5. Unique Constraints


### 1.15.6. Indexes

### 1.15.6.1. idx_auditlog_timestamp
#### 1.15.6.1.2. Columns

- timestamp

#### 1.15.6.1.3. Type
BTree

### 1.15.6.2. idx_auditlog_eventtype
#### 1.15.6.2.2. Columns

- eventType

#### 1.15.6.2.3. Type
BTree

### 1.15.6.3. idx_auditlog_targetentity_targetid
#### 1.15.6.3.2. Columns

- targetEntity
- targetId

#### 1.15.6.3.3. Type
BTree


## 1.16. CampaignPerformanceMV
Materialized View: Pre-aggregates campaign performance metrics. Refreshed periodically. Optimization Note: Use read replicas for serving dashboard data derived from this.

### 1.16.3. Attributes

### 1.16.3.1. campaignId
#### 1.16.3.1.2. Type
UUID

#### 1.16.3.1.3. Is Required
True

#### 1.16.3.1.4. Is Primary Key
True

#### 1.16.3.1.5. Is Foreign Key
True

#### 1.16.3.1.6. Constraints

- REFERENCES Campaign(id) ON DELETE CASCADE

### 1.16.3.2. campaignName
#### 1.16.3.2.2. Type
VARCHAR

#### 1.16.3.2.3. Is Required
True

#### 1.16.3.2.4. Size
100

### 1.16.3.3. totalApplications
#### 1.16.3.3.2. Type
INT

#### 1.16.3.3.3. Is Required
True

#### 1.16.3.3.4. Default Value
0

### 1.16.3.4. approvedApplications
#### 1.16.3.4.2. Type
INT

#### 1.16.3.4.3. Is Required
True

#### 1.16.3.4.4. Default Value
0

### 1.16.3.5. totalSubmissions
#### 1.16.3.5.2. Type
INT

#### 1.16.3.5.3. Is Required
True

#### 1.16.3.5.4. Default Value
0

### 1.16.3.6. approvedSubmissions
#### 1.16.3.6.2. Type
INT

#### 1.16.3.6.3. Is Required
True

#### 1.16.3.6.4. Default Value
0

### 1.16.3.7. totalEngagement
#### 1.16.3.7.2. Type
BIGINT

#### 1.16.3.7.3. Is Required
False

#### 1.16.3.7.4. Default Value
0

### 1.16.3.8. lastRefreshedAt
#### 1.16.3.8.2. Type
DateTime

#### 1.16.3.8.3. Is Required
True

#### 1.16.3.8.4. Default Value
CURRENT_TIMESTAMP


### 1.16.4. Primary Keys

- campaignId

### 1.16.5. Unique Constraints


### 1.16.6. Indexes




---

# 2. Relations

## 2.1. Influencer_SocialMedia
### 2.1.2. Source Entity
InfluencerProfile

### 2.1.3. Target Entity
SocialMediaProfile

### 2.1.4. Type
OneToMany

### 2.1.5. Source Multiplicity
1

### 2.1.6. Target Multiplicity
*

### 2.1.7. Cascade Delete
True

### 2.1.8. Is Identifying
True

### 2.1.9. On Delete
Cascade

### 2.1.10. On Update
Cascade

## 2.2. Influencer_KYC
### 2.2.2. Source Entity
InfluencerProfile

### 2.2.3. Target Entity
KYCData

### 2.2.4. Type
OneToMany

### 2.2.5. Source Multiplicity
1

### 2.2.6. Target Multiplicity
*

### 2.2.7. Cascade Delete
True

### 2.2.8. Is Identifying
True

### 2.2.9. On Delete
Cascade

### 2.2.10. On Update
Cascade

## 2.3. Influencer_BankAccount
### 2.3.2. Source Entity
InfluencerProfile

### 2.3.3. Target Entity
BankAccount

### 2.3.4. Type
OneToMany

### 2.3.5. Source Multiplicity
1

### 2.3.6. Target Multiplicity
*

### 2.3.7. Cascade Delete
True

### 2.3.8. Is Identifying
True

### 2.3.9. On Delete
Cascade

### 2.3.10. On Update
Cascade

## 2.4. Influencer_TermsConsent
### 2.4.2. Source Entity
InfluencerProfile

### 2.4.3. Target Entity
TermsConsent

### 2.4.4. Type
OneToMany

### 2.4.5. Source Multiplicity
1

### 2.4.6. Target Multiplicity
*

### 2.4.7. Cascade Delete
True

### 2.4.8. Is Identifying
True

### 2.4.9. On Delete
Cascade

### 2.4.10. On Update
Cascade

## 2.5. Campaign_Application
### 2.5.2. Source Entity
Campaign

### 2.5.3. Target Entity
CampaignApplication

### 2.5.4. Type
OneToMany

### 2.5.5. Source Multiplicity
1

### 2.5.6. Target Multiplicity
*

### 2.5.7. Cascade Delete
True

### 2.5.8. Is Identifying
True

### 2.5.9. On Delete
Cascade

### 2.5.10. On Update
Cascade

## 2.6. Application_Submission
### 2.6.2. Source Entity
CampaignApplication

### 2.6.3. Target Entity
ContentSubmission

### 2.6.4. Type
OneToMany

### 2.6.5. Source Multiplicity
1

### 2.6.6. Target Multiplicity
*

### 2.6.7. Cascade Delete
True

### 2.6.8. Is Identifying
True

### 2.6.9. On Delete
Cascade

### 2.6.10. On Update
Cascade

## 2.7. ImageRequest_GeneratedImage
### 2.7.2. Source Entity
AIImageGenerationRequest

### 2.7.3. Target Entity
GeneratedImage

### 2.7.4. Type
OneToMany

### 2.7.5. Source Multiplicity
1

### 2.7.6. Target Multiplicity
*

### 2.7.7. Cascade Delete
True

### 2.7.8. Is Identifying
True

### 2.7.9. On Delete
Cascade

### 2.7.10. On Update
Cascade

## 2.8. ImageModel_Request
### 2.8.2. Source Entity
AIImageModel

### 2.8.3. Target Entity
AIImageGenerationRequest

### 2.8.4. Type
OneToMany

### 2.8.5. Source Multiplicity
1

### 2.8.6. Target Multiplicity
*

### 2.8.7. Cascade Delete
False

### 2.8.8. Is Identifying
False

### 2.8.9. On Delete
Restrict

### 2.8.10. On Update
Cascade

## 2.9. Influencer_Payment
### 2.9.2. Source Entity
InfluencerProfile

### 2.9.3. Target Entity
PaymentRecord

### 2.9.4. Type
OneToMany

### 2.9.5. Source Multiplicity
1

### 2.9.6. Target Multiplicity
*

### 2.9.7. Cascade Delete
False

### 2.9.8. Is Identifying
False

### 2.9.9. On Delete
Restrict

### 2.9.10. On Update
Cascade

## 2.10. Application_Reviewer
### 2.10.2. Source Entity
CampaignApplication

### 2.10.3. Target Entity
AuditLog

### 2.10.4. Type
OneToMany

### 2.10.5. Source Multiplicity
1

### 2.10.6. Target Multiplicity
*

### 2.10.7. Cascade Delete
False

### 2.10.8. Is Identifying
False

### 2.10.9. On Delete
SetNull

### 2.10.10. On Update
Cascade

## 2.11. Campaign_ImageRequest
### 2.11.2. Source Entity
Campaign

### 2.11.3. Target Entity
AIImageGenerationRequest

### 2.11.4. Type
OneToMany

### 2.11.5. Source Multiplicity
0..1

### 2.11.6. Target Multiplicity
*

### 2.11.7. Cascade Delete
False

### 2.11.8. Is Identifying
False

### 2.11.9. On Delete
SetNull

### 2.11.10. On Update
Cascade

## 2.12. Influencer_Application
### 2.12.2. Source Entity
InfluencerProfile

### 2.12.3. Target Entity
CampaignApplication

### 2.12.4. Type
OneToMany

### 2.12.5. Source Multiplicity
1

### 2.12.6. Target Multiplicity
*

### 2.12.7. Cascade Delete
True

### 2.12.8. Is Identifying
True

### 2.12.9. On Delete
Cascade

### 2.12.10. On Update
Cascade

## 2.13. Submission_Image
### 2.13.2. Source Entity
ContentSubmission

### 2.13.3. Target Entity
GeneratedImage

### 2.13.4. Type
OneToOne

### 2.13.5. Source Multiplicity
0..1

### 2.13.6. Target Multiplicity
0..1

### 2.13.7. Cascade Delete
False

### 2.13.8. Is Identifying
False

### 2.13.9. On Delete
SetNull

### 2.13.10. On Update
Cascade

## 2.14. Campaign_Payment
### 2.14.2. Source Entity
Campaign

### 2.14.3. Target Entity
PaymentRecord

### 2.14.4. Type
OneToMany

### 2.14.5. Source Multiplicity
0..1

### 2.14.6. Target Multiplicity
*

### 2.14.7. Cascade Delete
False

### 2.14.8. Is Identifying
False

### 2.14.9. On Delete
SetNull

### 2.14.10. On Update
Cascade

## 2.15. Influencer_Has_AreasOfInfluence
### 2.15.2. Source Entity
InfluencerProfile

### 2.15.3. Target Entity
AreaOfInfluence

### 2.15.4. Type
ManyToMany

### 2.15.5. Source Multiplicity
*

### 2.15.6. Target Multiplicity
*

### 2.15.7. Join Table
### 2.15.7. Influencer_AreaOfInfluence
#### 2.15.7.2. Columns

- **Name:** influencerProfileId  
**Type:** UUID  
**References:** InfluencerProfile  
- **Name:** areaOfInfluenceId  
**Type:** UUID  
**References:** AreaOfInfluence  

### 2.15.8. On Delete
Cascade

### 2.15.9. On Update
Cascade



---

