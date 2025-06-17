# Specification

# 1. Database Design

## 1.1. InfluencerProfile
Stores influencer profile information. Linked to the Odoo user account. Optimization Note: For 'audienceDemographics' (JSON type), use database-specific JSON indexing (e.g., GIN index in PostgreSQL for JSONB). Frequent queries on 'kycStatus' and 'accountStatus' are supported by BTree indexes. CreatedAt index supports historical analysis.

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

### 1.1.3.2. userId
Foreign key linking to the Odoo 'res.users' table.

#### 1.1.3.2.2. Type
UUID

#### 1.1.3.2.3. Is Required
True

#### 1.1.3.2.4. Is Unique
True

#### 1.1.3.2.5. Is Foreign Key
True

#### 1.1.3.2.6. Constraints

- REFERENCES res_users(id) ON DELETE CASCADE

### 1.1.3.3. fullName
#### 1.1.3.3.2. Type
VARCHAR

#### 1.1.3.3.3. Is Required
True

#### 1.1.3.3.4. Size
100

### 1.1.3.4. email
Used as a primary identifier and login.

#### 1.1.3.4.2. Type
VARCHAR

#### 1.1.3.4.3. Is Required
True

#### 1.1.3.4.4. Is Unique
True

#### 1.1.3.4.5. Size
100

### 1.1.3.5. phone
#### 1.1.3.5.2. Type
VARCHAR

#### 1.1.3.5.3. Is Required
False

#### 1.1.3.5.4. Size
20

### 1.1.3.6. residentialAddress
#### 1.1.3.6.2. Type
VARCHAR

#### 1.1.3.6.3. Is Required
False

#### 1.1.3.6.4. Size
255

### 1.1.3.7. audienceDemographics
JSON or JSONB field storing audience demographic data (e.g., age, gender, location distribution). Indexed for queryability.

#### 1.1.3.7.2. Type
JSON

#### 1.1.3.7.3. Is Required
False

### 1.1.3.8. kycStatus
Current status of KYC verification (e.g., 'pending', 'in_review', 'approved', 'rejected'). Indexed for filtering.

#### 1.1.3.8.2. Type
VARCHAR

#### 1.1.3.8.3. Is Required
True

#### 1.1.3.8.4. Size
20

#### 1.1.3.8.5. Default Value
'pending'

### 1.1.3.9. accountStatus
Overall account status (e.g., 'inactive', 'active', 'suspended'). Indexed for filtering.

#### 1.1.3.9.2. Type
VARCHAR

#### 1.1.3.9.3. Is Required
True

#### 1.1.3.9.4. Size
20

#### 1.1.3.9.5. Default Value
'inactive'

### 1.1.3.10. createdAt
Timestamp when the profile was created.

#### 1.1.3.10.2. Type
DateTime

#### 1.1.3.10.3. Is Required
True

#### 1.1.3.10.4. Default Value
CURRENT_TIMESTAMP

### 1.1.3.11. updatedAt
Timestamp when the profile was last updated.

#### 1.1.3.11.2. Type
DateTime

#### 1.1.3.11.3. Is Required
True

#### 1.1.3.11.4. Default Value
CURRENT_TIMESTAMP


### 1.1.4. Primary Keys

- id

### 1.1.5. Unique Constraints

### 1.1.5.1. uq_influencerprofile_email
#### 1.1.5.1.2. Columns

- email

### 1.1.5.2. uq_influencerprofile_userid
Ensures a one-to-one relationship between InfluencerProfile and res.users.

#### 1.1.5.2.2. Columns

- userId


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
Stores distinct areas of influence (Normalized from InfluencerProfile). Optimization Note: Consider application-level or distributed caching for this rarely changing lookup data.

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
The name of the area of influence (e.g., 'Fashion', 'Gaming'). Indexed for searches.

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
Join table linking influencers to their areas of influence. Represents a Many-to-Many relationship.

### 1.3.3. Attributes

### 1.3.3.1. influencerProfileId
Foreign key linking to the InfluencerProfile.

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
Foreign key linking to the AreaOfInfluence.

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

### 1.3.6.1. idx_influencerareaofinfluence_areaid
Index for querying influencers by area.

#### 1.3.6.1.2. Columns

- areaOfInfluenceId

#### 1.3.6.1.3. Type
BTree


## 1.4. SocialMediaProfile
Stores influencer social media accounts and verification status. Optimization Note: Indexed by influencerProfileId for quick retrieval of all profiles for a given influencer.

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
Foreign key linking to the InfluencerProfile.

#### 1.4.3.2.2. Type
UUID

#### 1.4.3.2.3. Is Required
True

#### 1.4.3.2.4. Is Foreign Key
True

#### 1.4.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.4.3.3. platform
Social media platform (e.g., 'Instagram', 'TikTok').

#### 1.4.3.3.2. Type
VARCHAR

#### 1.4.3.3.3. Is Required
True

#### 1.4.3.3.4. Size
50

### 1.4.3.4. handle
The influencer's handle or username on the platform.

#### 1.4.3.4.2. Type
VARCHAR

#### 1.4.3.4.3. Is Required
True

#### 1.4.3.4.4. Size
100

### 1.4.3.5. url
Direct URL to the social media profile.

#### 1.4.3.5.2. Type
VARCHAR

#### 1.4.3.5.3. Is Required
False

#### 1.4.3.5.4. Size
255

### 1.4.3.6. verificationStatus
Status of account ownership verification (e.g., 'pending', 'verified', 'failed').

#### 1.4.3.6.2. Type
VARCHAR

#### 1.4.3.6.3. Is Required
True

#### 1.4.3.6.4. Size
20

#### 1.4.3.6.5. Default Value
'pending'

### 1.4.3.7. verificationMethod
Method used for verification (e.g., 'oauth', 'code_in_bio', 'manual').

#### 1.4.3.7.2. Type
VARCHAR

#### 1.4.3.7.3. Is Required
False

#### 1.4.3.7.4. Size
50

### 1.4.3.8. verificationCode
Code used for verification if applicable.

#### 1.4.3.8.2. Type
VARCHAR

#### 1.4.3.8.3. Is Required
False

#### 1.4.3.8.4. Size
50

### 1.4.3.9. verifiedAt
Timestamp when the account was successfully verified.

#### 1.4.3.9.2. Type
DateTime

#### 1.4.3.9.3. Is Required
False

### 1.4.3.10. audienceMetrics
JSON or JSONB field storing fetched or calculated audience metrics (e.g., follower_count, engagement_rate).

#### 1.4.3.10.2. Type
JSON

#### 1.4.3.10.3. Is Required
False

### 1.4.3.11. lastFetchedAt
Timestamp when metrics were last fetched (if using API integration).

#### 1.4.3.11.2. Type
DateTime

#### 1.4.3.11.3. Is Required
False

### 1.4.3.12. createdAt
Timestamp when the record was created.

#### 1.4.3.12.2. Type
DateTime

#### 1.4.3.12.3. Is Required
True

#### 1.4.3.12.4. Default Value
CURRENT_TIMESTAMP

### 1.4.3.13. updatedAt
Timestamp when the record was last updated.

#### 1.4.3.13.2. Type
DateTime

#### 1.4.3.13.3. Is Required
True

#### 1.4.3.13.4. Default Value
CURRENT_TIMESTAMP


### 1.4.4. Primary Keys

- id

### 1.4.5. Unique Constraints

### 1.4.5.1. uq_socialmediaprofile_platform_handle
Ensures uniqueness of a handle per platform.

#### 1.4.5.1.2. Columns

- platform
- handle


### 1.4.6. Indexes

### 1.4.6.1. idx_socialmediaprofile_influencerid
#### 1.4.6.1.2. Columns

- influencerProfileId

#### 1.4.6.1.3. Type
BTree

### 1.4.6.2. idx_socialmediaprofile_verificationstatus
Index for filtering by verification status.

#### 1.4.6.2.2. Columns

- verificationStatus

#### 1.4.6.2.3. Type
BTree


## 1.5. KYCData
Stores KYC verification information and links to uploaded documents. Sensitive data is stored securely (encrypted at rest). Optimization Note: Indexed by influencerProfileId for quick access to an influencer's KYC history.

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
Foreign key linking to the InfluencerProfile.

#### 1.5.3.2.2. Type
UUID

#### 1.5.3.2.3. Is Required
True

#### 1.5.3.2.4. Is Foreign Key
True

#### 1.5.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.5.3.3. documentType
Type of document submitted (e.g., 'passport', 'driver_license').

#### 1.5.3.3.2. Type
VARCHAR

#### 1.5.3.3.3. Is Required
True

#### 1.5.3.3.4. Size
50

### 1.5.3.4. documentFrontUrl
Secure storage URL or identifier for the front of the document. Stored securely (e.g., Odoo filestore identifier, cloud storage URL).

#### 1.5.3.4.2. Type
TEXT

#### 1.5.3.4.3. Is Required
True

### 1.5.3.5. documentBackUrl
Secure storage URL or identifier for the back of the document (if applicable).

#### 1.5.3.5.2. Type
TEXT

#### 1.5.3.5.3. Is Required
False

### 1.5.3.6. verificationMethod
Method of verification (e.g., 'manual', 'third_party_api').

#### 1.5.3.6.2. Type
VARCHAR

#### 1.5.3.6.3. Is Required
True

#### 1.5.3.6.4. Size
50

### 1.5.3.7. verificationStatus
Status of the verification attempt (e.g., 'pending', 'approved', 'rejected', 'needs_more_info'). Indexed for filtering.

#### 1.5.3.7.2. Type
VARCHAR

#### 1.5.3.7.3. Is Required
True

#### 1.5.3.7.4. Size
20

#### 1.5.3.7.5. Default Value
'pending'

### 1.5.3.8. reviewerUserId
Foreign key linking to the Odoo user (admin) who reviewed the submission, if applicable.

#### 1.5.3.8.2. Type
UUID

#### 1.5.3.8.3. Is Required
False

#### 1.5.3.8.4. Is Foreign Key
True

#### 1.5.3.8.5. Constraints

- REFERENCES res_users(id) ON DELETE SET NULL

### 1.5.3.9. reviewedAt
Timestamp when the submission was reviewed.

#### 1.5.3.9.2. Type
DateTime

#### 1.5.3.9.3. Is Required
False

### 1.5.3.10. notes
Internal notes from the reviewer.

#### 1.5.3.10.2. Type
TEXT

#### 1.5.3.10.3. Is Required
False

### 1.5.3.11. createdAt
Timestamp when the submission was created.

#### 1.5.3.11.2. Type
DateTime

#### 1.5.3.11.3. Is Required
True

#### 1.5.3.11.4. Default Value
CURRENT_TIMESTAMP

### 1.5.3.12. updatedAt
Timestamp when the submission was last updated.

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
Index for retrieving KYC data by influencer.

#### 1.5.6.1.2. Columns

- influencerProfileId

#### 1.5.6.1.3. Type
BTree

### 1.5.6.2. idx_kycdata_verificationstatus
Index for filtering KYC data by status.

#### 1.5.6.2.2. Columns

- verificationStatus

#### 1.5.6.2.3. Type
BTree

### 1.5.6.3. idx_kycdata_revieweruserid
Index for retrieving KYC data reviewed by a specific user.

#### 1.5.6.3.2. Columns

- reviewerUserId

#### 1.5.6.3.3. Type
BTree


## 1.6. BankAccount
Stores influencer bank account details. Sensitive financial data must be encrypted at rest. Optimization Note: Indexed by influencerProfileId for quick access to an influencer's bank accounts.

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
Foreign key linking to the InfluencerProfile.

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
Bank account number. Must be stored encrypted.

#### 1.6.3.4.2. Type
TEXT

#### 1.6.3.4.3. Is Required
True

### 1.6.3.5. bankName
#### 1.6.3.5.2. Type
VARCHAR

#### 1.6.3.5.3. Is Required
True

#### 1.6.3.5.4. Size
100

### 1.6.3.6. routingNumber
Routing number. Must be stored encrypted if applicable.

#### 1.6.3.6.2. Type
TEXT

#### 1.6.3.6.3. Is Required
False

### 1.6.3.7. iban
IBAN. Must be stored encrypted if applicable.

#### 1.6.3.7.2. Type
TEXT

#### 1.6.3.7.3. Is Required
False

### 1.6.3.8. swiftCode
SWIFT code. Must be stored encrypted if applicable.

#### 1.6.3.8.2. Type
TEXT

#### 1.6.3.8.3. Is Required
False

### 1.6.3.9. verificationStatus
Status of account verification (e.g., 'pending', 'verified', 'failed').

#### 1.6.3.9.2. Type
VARCHAR

#### 1.6.3.9.3. Is Required
True

#### 1.6.3.9.4. Size
20

#### 1.6.3.9.5. Default Value
'pending'

### 1.6.3.10. verificationMethod
Method used for verification (e.g., 'micro_deposit', 'third_party_api', 'manual').

#### 1.6.3.10.2. Type
VARCHAR

#### 1.6.3.10.3. Is Required
False

#### 1.6.3.10.4. Size
50

### 1.6.3.11. isPrimary
Flag indicating if this is the primary account for payouts.

#### 1.6.3.11.2. Type
BOOLEAN

#### 1.6.3.11.3. Is Required
True

#### 1.6.3.11.4. Default Value
false

### 1.6.3.12. createdAt
Timestamp when the record was created.

#### 1.6.3.12.2. Type
DateTime

#### 1.6.3.12.3. Is Required
True

#### 1.6.3.12.4. Default Value
CURRENT_TIMESTAMP

### 1.6.3.13. updatedAt
Timestamp when the record was last updated.

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
Index for retrieving bank accounts by influencer.

#### 1.6.6.1.2. Columns

- influencerProfileId

#### 1.6.6.1.3. Type
BTree

### 1.6.6.2. idx_bankaccount_influencer_isprimary
Index for finding the primary bank account for an influencer.

#### 1.6.6.2.2. Columns

- influencerProfileId
- isPrimary

#### 1.6.6.2.3. Type
BTree

### 1.6.6.3. idx_bankaccount_verificationstatus
Index for filtering by verification status.

#### 1.6.6.3.2. Columns

- verificationStatus

#### 1.6.6.3.3. Type
BTree


## 1.7. Campaign
Stores marketing campaign details. Optimization Note: Cache details of 'Published/Open' campaigns. 'targetCriteria' JSON is indexed for filtering. Full-text indexes support search on name, description, requirements. Status and date indexes support filtering and sorting for discovery.

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
Campaign name. Indexed for search.

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
Detailed campaign description. Indexed for search.

#### 1.7.3.3.2. Type
TEXT

#### 1.7.3.3.3. Is Required
True

#### 1.7.3.3.4. Index Type
FullText

### 1.7.3.4. brandClient
Name of the brand or client.

#### 1.7.3.4.2. Type
VARCHAR

#### 1.7.3.4.3. Is Required
True

#### 1.7.3.4.4. Size
100

### 1.7.3.5. goals
Campaign goals and KPIs.

#### 1.7.3.5.2. Type
TEXT

#### 1.7.3.5.3. Is Required
True

### 1.7.3.6. targetCriteria
JSON or JSONB field specifying target influencer criteria (e.g., audience niche, location). Indexed for filtering influencer discovery.

#### 1.7.3.6.2. Type
JSON

#### 1.7.3.6.3. Is Required
True

#### 1.7.3.6.4. Index Type
GIN

### 1.7.3.7. contentRequirements
Specific requirements for content creation. Indexed for search.

#### 1.7.3.7.2. Type
TEXT

#### 1.7.3.7.3. Is Required
True

#### 1.7.3.7.4. Index Type
FullText

### 1.7.3.8. budget
Total campaign budget.

#### 1.7.3.8.2. Type
DECIMAL

#### 1.7.3.8.3. Is Required
False

#### 1.7.3.8.4. Precision
15

#### 1.7.3.8.5. Scale
2

### 1.7.3.9. compensationModel
Type of compensation (e.g., 'flat_fee', 'cpm', 'cpa'). Indexed for filtering.

#### 1.7.3.9.2. Type
VARCHAR

#### 1.7.3.9.3. Is Required
True

#### 1.7.3.9.4. Size
50

### 1.7.3.10. submissionDeadline
Deadline for content submission. Indexed.

#### 1.7.3.10.2. Type
DateTime

#### 1.7.3.10.3. Is Required
True

### 1.7.3.11. startDate
Campaign start date. Indexed.

#### 1.7.3.11.2. Type
DateTime

#### 1.7.3.11.3. Is Required
True

### 1.7.3.12. endDate
Campaign end date. Indexed.

#### 1.7.3.12.2. Type
DateTime

#### 1.7.3.12.3. Is Required
True

### 1.7.3.13. usageRights
Details on usage rights for submitted content.

#### 1.7.3.13.2. Type
TEXT

#### 1.7.3.13.3. Is Required
True

### 1.7.3.14. status
Campaign status (e.g., 'draft', 'published', 'open', 'closed', 'completed'). Indexed for filtering.

#### 1.7.3.14.2. Type
VARCHAR

#### 1.7.3.14.3. Is Required
True

#### 1.7.3.14.4. Size
20

#### 1.7.3.14.5. Default Value
'draft'

### 1.7.3.15. actualPerformanceMetrics
JSON or JSONB field storing actual performance data for the campaign (e.g., 'total_reach', 'total_engagement').

#### 1.7.3.15.2. Type
JSON

#### 1.7.3.15.3. Is Required
False

### 1.7.3.16. createdAt
Timestamp when the campaign was created.

#### 1.7.3.16.2. Type
DateTime

#### 1.7.3.16.3. Is Required
True

#### 1.7.3.16.4. Default Value
CURRENT_TIMESTAMP

### 1.7.3.17. updatedAt
Timestamp when the campaign was last updated.

#### 1.7.3.17.2. Type
DateTime

#### 1.7.3.17.3. Is Required
True

#### 1.7.3.17.4. Default Value
CURRENT_TIMESTAMP


### 1.7.4. Primary Keys

- id

### 1.7.5. Unique Constraints

### 1.7.5.1. uq_campaign_name
Ensures campaign names are unique.

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
Stores influencer applications to campaigns. Optimization Note: Indexed by campaign and influencer for efficient retrieval and uniqueness constraint. Indexed by status for workflow management.

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
Foreign key linking to the Campaign.

#### 1.8.3.2.2. Type
UUID

#### 1.8.3.2.3. Is Required
True

#### 1.8.3.2.4. Is Foreign Key
True

#### 1.8.3.2.5. Constraints

- REFERENCES Campaign(id) ON DELETE CASCADE

### 1.8.3.3. influencerProfileId
Foreign key linking to the InfluencerProfile.

#### 1.8.3.3.2. Type
UUID

#### 1.8.3.3.3. Is Required
True

#### 1.8.3.3.4. Is Foreign Key
True

#### 1.8.3.3.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.8.3.4. proposal
Influencer's application proposal text.

#### 1.8.3.4.2. Type
TEXT

#### 1.8.3.4.3. Is Required
False

### 1.8.3.5. status
Status of the application (e.g., 'submitted', 'approved', 'rejected', 'withdrawn'). Indexed for filtering.

#### 1.8.3.5.2. Type
VARCHAR

#### 1.8.3.5.3. Is Required
True

#### 1.8.3.5.4. Size
20

#### 1.8.3.5.5. Default Value
'submitted'

### 1.8.3.6. submittedAt
Timestamp when the application was submitted.

#### 1.8.3.6.2. Type
DateTime

#### 1.8.3.6.3. Is Required
True

#### 1.8.3.6.4. Default Value
CURRENT_TIMESTAMP

### 1.8.3.7. reviewedAt
Timestamp when the application was reviewed.

#### 1.8.3.7.2. Type
DateTime

#### 1.8.3.7.3. Is Required
False

### 1.8.3.8. reviewerUserId
Foreign key linking to the Odoo user (admin) who reviewed the application, if applicable.

#### 1.8.3.8.2. Type
UUID

#### 1.8.3.8.3. Is Required
False

#### 1.8.3.8.4. Is Foreign Key
True

#### 1.8.3.8.5. Constraints

- REFERENCES res_users(id) ON DELETE SET NULL

### 1.8.3.9. rejectionReason
Reason for rejection, if applicable.

#### 1.8.3.9.2. Type
TEXT

#### 1.8.3.9.3. Is Required
False

### 1.8.3.10. createdAt
Timestamp when the record was created.

#### 1.8.3.10.2. Type
DateTime

#### 1.8.3.10.3. Is Required
True

#### 1.8.3.10.4. Default Value
CURRENT_TIMESTAMP

### 1.8.3.11. updatedAt
Timestamp when the record was last updated.

#### 1.8.3.11.2. Type
DateTime

#### 1.8.3.11.3. Is Required
True

#### 1.8.3.11.4. Default Value
CURRENT_TIMESTAMP


### 1.8.4. Primary Keys

- id

### 1.8.5. Unique Constraints

### 1.8.5.1. uq_campaignapplication_campaign_influencer
Ensures an influencer can only apply to a campaign once.

#### 1.8.5.1.2. Columns

- campaignId
- influencerProfileId


### 1.8.6. Indexes

### 1.8.6.1. idx_campaignapplication_campaign_status
Index for finding applications for a campaign by status.

#### 1.8.6.1.2. Columns

- campaignId
- status

#### 1.8.6.1.3. Type
BTree

### 1.8.6.2. idx_campaignapplication_influencer_status
Index for finding applications by an influencer by status.

#### 1.8.6.2.2. Columns

- influencerProfileId
- status

#### 1.8.6.2.3. Type
BTree

### 1.8.6.3. idx_campaignapplication_revieweruserid
Index for retrieving applications reviewed by a specific user.

#### 1.8.6.3.2. Columns

- reviewerUserId

#### 1.8.6.3.3. Type
BTree


## 1.9. ContentSubmission
Stores content submitted by influencers for campaigns. Optimization Note: Indexed by campaignApplicationId for retrieving submissions for a specific application. Indexed by reviewStatus for managing review workflow. Consider range partitioning by 'submissionDate' if the table is expected to grow very large.

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
Foreign key linking to the CampaignApplication.

#### 1.9.3.2.2. Type
UUID

#### 1.9.3.2.3. Is Required
True

#### 1.9.3.2.4. Is Foreign Key
True

#### 1.9.3.2.5. Constraints

- REFERENCES CampaignApplication(id) ON DELETE CASCADE

### 1.9.3.3. generatedImageId
Foreign key linking to the GeneratedImage, if this submission is an AI-generated image. ON DELETE SET NULL allows the submission record to persist even if the generated image is deleted (e.g., via retention policy).

#### 1.9.3.3.2. Type
UUID

#### 1.9.3.3.3. Is Required
False

#### 1.9.3.3.4. Is Foreign Key
True

#### 1.9.3.3.5. Constraints

- REFERENCES GeneratedImage(id) ON DELETE SET NULL

### 1.9.3.4. contentUrl
Secure storage URL or identifier for the submitted content (e.g., link to uploaded file in filestore/cloud storage, or link to social media post). If it's an AI image, this might duplicate GeneratedImage.storageUrl, but represents the content *as submitted*.

#### 1.9.3.4.2. Type
TEXT

#### 1.9.3.4.3. Is Required
True

### 1.9.3.5. fileType
File type (e.g., 'image/jpeg', 'video/mp4') or content type ('social_media_link').

#### 1.9.3.5.2. Type
VARCHAR

#### 1.9.3.5.3. Is Required
False

#### 1.9.3.5.4. Size
50

### 1.9.3.6. fileSize
File size in bytes, if applicable.

#### 1.9.3.6.2. Type
BIGINT

#### 1.9.3.6.3. Is Required
False

### 1.9.3.7. submissionDate
Timestamp when the content was submitted. Indexed for time-based queries and potential partitioning.

#### 1.9.3.7.2. Type
DateTime

#### 1.9.3.7.3. Is Required
True

#### 1.9.3.7.4. Default Value
CURRENT_TIMESTAMP

### 1.9.3.8. reviewStatus
Status of the content review (e.g., 'pending', 'approved', 'rejected', 'needs_revision'). Indexed for filtering.

#### 1.9.3.8.2. Type
VARCHAR

#### 1.9.3.8.3. Is Required
True

#### 1.9.3.8.4. Size
20

#### 1.9.3.8.5. Default Value
'pending'

### 1.9.3.9. feedback
Feedback from the reviewer.

#### 1.9.3.9.2. Type
TEXT

#### 1.9.3.9.3. Is Required
False

### 1.9.3.10. reviewedByUserId
Foreign key linking to the Odoo user (admin) who reviewed the content, if applicable.

#### 1.9.3.10.2. Type
UUID

#### 1.9.3.10.3. Is Required
False

#### 1.9.3.10.4. Is Foreign Key
True

#### 1.9.3.10.5. Constraints

- REFERENCES res_users(id) ON DELETE SET NULL

### 1.9.3.11. reviewedAt
Timestamp when the content was reviewed.

#### 1.9.3.11.2. Type
DateTime

#### 1.9.3.11.3. Is Required
False

### 1.9.3.12. version
Version number for revisions.

#### 1.9.3.12.2. Type
INT

#### 1.9.3.12.3. Is Required
True

#### 1.9.3.12.4. Default Value
1

### 1.9.3.13. createdAt
Timestamp when the record was created.

#### 1.9.3.13.2. Type
DateTime

#### 1.9.3.13.3. Is Required
True

#### 1.9.3.13.4. Default Value
CURRENT_TIMESTAMP

### 1.9.3.14. updatedAt
Timestamp when the record was last updated.

#### 1.9.3.14.2. Type
DateTime

#### 1.9.3.14.3. Is Required
True

#### 1.9.3.14.4. Default Value
CURRENT_TIMESTAMP


### 1.9.4. Primary Keys

- id

### 1.9.5. Unique Constraints


### 1.9.6. Indexes

### 1.9.6.1. idx_contentsubmission_campaignapplicationid
Index for retrieving submissions by application.

#### 1.9.6.1.2. Columns

- campaignApplicationId

#### 1.9.6.1.3. Type
BTree

### 1.9.6.2. idx_contentsubmission_reviewstatus
Index for filtering submissions by review status.

#### 1.9.6.2.2. Columns

- reviewStatus

#### 1.9.6.2.3. Type
BTree

### 1.9.6.3. idx_contentsubmission_reviewedbyuserid
Index for retrieving submissions reviewed by a specific user.

#### 1.9.6.3.2. Columns

- reviewedByUserId

#### 1.9.6.3.3. Type
BTree

### 1.9.6.4. idx_contentsubmission_submissiondate
Index for time-based queries.

#### 1.9.6.4.2. Columns

- submissionDate

#### 1.9.6.4.3. Type
BTree

### 1.9.6.5. idx_contentsubmission_generatedimageid
Index for retrieving submissions linked to a generated image.

#### 1.9.6.5.2. Columns

- generatedImageId

#### 1.9.6.5.3. Type
BTree


## 1.10. AIImageModel
Stores available AI image generation models configured in the system. Optimization Note: Cache frequently accessed, rarely changing data like active models.

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
Unique name of the AI model (e.g., 'Flux_v1', 'SDXL_LoRA_StyleA').

#### 1.10.3.2.2. Type
VARCHAR

#### 1.10.3.2.3. Is Required
True

#### 1.10.3.2.4. Is Unique
True

#### 1.10.3.2.5. Size
50

### 1.10.3.3. description
Description of the model.

#### 1.10.3.3.2. Type
TEXT

#### 1.10.3.3.3. Is Required
False

### 1.10.3.4. triggerKeywords
Keywords that may trigger this model or be associated with it.

#### 1.10.3.4.2. Type
VARCHAR

#### 1.10.3.4.3. Is Required
False

#### 1.10.3.4.4. Size
255

### 1.10.3.5. isActive
Flag indicating if the model is currently active and available for use. Indexed for filtering.

#### 1.10.3.5.2. Type
BOOLEAN

#### 1.10.3.5.3. Is Required
True

#### 1.10.3.5.4. Default Value
true

### 1.10.3.6. externalModelId
Identifier used by the external AI service API, if applicable.

#### 1.10.3.6.2. Type
VARCHAR

#### 1.10.3.6.3. Is Required
False

#### 1.10.3.6.4. Size
100

### 1.10.3.7. createdAt
Timestamp when the record was created.

#### 1.10.3.7.2. Type
DateTime

#### 1.10.3.7.3. Is Required
True

#### 1.10.3.7.4. Default Value
CURRENT_TIMESTAMP

### 1.10.3.8. updatedAt
Timestamp when the record was last updated.

#### 1.10.3.8.2. Type
DateTime

#### 1.10.3.8.3. Is Required
True

#### 1.10.3.8.4. Default Value
CURRENT_TIMESTAMP


### 1.10.4. Primary Keys

- id

### 1.10.5. Unique Constraints

### 1.10.5.1. uq_aiimagemodel_name
Ensures model names are unique.

#### 1.10.5.1.2. Columns

- name


### 1.10.6. Indexes

### 1.10.6.1. idx_aiimagemodel_isactive
Index for finding active models.

#### 1.10.6.1.2. Columns

- isActive

#### 1.10.6.1.3. Type
BTree


## 1.11. AIImageGenerationRequest
Stores AI image generation requests initiated by users. Optimization Note: Indexed by userId and status for tracking user requests and workflow processing.

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
Foreign key linking to the Odoo user who initiated the request.

#### 1.11.3.2.2. Type
UUID

#### 1.11.3.2.3. Is Required
True

#### 1.11.3.2.4. Is Foreign Key
True

#### 1.11.3.2.5. Constraints

- REFERENCES res_users(id) ON DELETE CASCADE

### 1.11.3.3. influencerProfileId
Foreign key linking to the InfluencerProfile associated with the user (redundant with userId if 1:1 user-influencer, but useful if a user can manage multiple profiles or for clarity).

#### 1.11.3.3.2. Type
UUID

#### 1.11.3.3.3. Is Required
True

#### 1.11.3.3.4. Is Foreign Key
True

#### 1.11.3.3.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.11.3.4. campaignId
Foreign key linking to the Campaign this request is associated with, if any.

#### 1.11.3.4.2. Type
UUID

#### 1.11.3.4.3. Is Required
False

#### 1.11.3.4.4. Is Foreign Key
True

#### 1.11.3.4.5. Constraints

- REFERENCES Campaign(id) ON DELETE SET NULL

### 1.11.3.5. prompt
The text prompt used for generation.

#### 1.11.3.5.2. Type
TEXT

#### 1.11.3.5.3. Is Required
True

### 1.11.3.6. negativePrompt
The negative prompt used for generation.

#### 1.11.3.6.2. Type
TEXT

#### 1.11.3.6.3. Is Required
False

### 1.11.3.7. modelId
Foreign key linking to the AIImageModel used.

#### 1.11.3.7.2. Type
UUID

#### 1.11.3.7.3. Is Required
True

#### 1.11.3.7.4. Is Foreign Key
True

#### 1.11.3.7.5. Constraints

- REFERENCES AIImageModel(id) ON DELETE RESTRICT

### 1.11.3.8. resolution
Image resolution requested (e.g., '512x512', '1024x1024').

#### 1.11.3.8.2. Type
VARCHAR

#### 1.11.3.8.3. Is Required
True

#### 1.11.3.8.4. Size
20

### 1.11.3.9. aspectRatio
Aspect ratio (e.g., '1:1', '16:9').

#### 1.11.3.9.2. Type
VARCHAR

#### 1.11.3.9.3. Is Required
True

#### 1.11.3.9.4. Size
10

### 1.11.3.10. seed
Seed value for reproducibility.

#### 1.11.3.10.2. Type
BIGINT

#### 1.11.3.10.3. Is Required
False

### 1.11.3.11. inferenceSteps
Number of inference steps.

#### 1.11.3.11.2. Type
INT

#### 1.11.3.11.3. Is Required
False

### 1.11.3.12. cfgScale
CFG Scale value.

#### 1.11.3.12.2. Type
DECIMAL

#### 1.11.3.12.3. Is Required
False

#### 1.11.3.12.4. Precision
3

#### 1.11.3.12.5. Scale
1

### 1.11.3.13. status
Current status of the request (e.g., 'queued', 'processing', 'completed', 'failed', 'cancelled'). Indexed for workflow management.

#### 1.11.3.13.2. Type
VARCHAR

#### 1.11.3.13.3. Is Required
True

#### 1.11.3.13.4. Size
20

#### 1.11.3.13.5. Default Value
'queued'

### 1.11.3.14. intendedUse
Intended use of the generated image(s) (e.g., 'personal', 'campaign'). Used for retention policy.

#### 1.11.3.14.2. Type
VARCHAR

#### 1.11.3.14.3. Is Required
True

#### 1.11.3.14.4. Size
30

#### 1.11.3.14.5. Default Value
'personal'

### 1.11.3.15. errorDetails
Details if the request failed.

#### 1.11.3.15.2. Type
TEXT

#### 1.11.3.15.3. Is Required
False

### 1.11.3.16. n8nExecutionId
Identifier for the corresponding execution in N8N, for tracing.

#### 1.11.3.16.2. Type
VARCHAR

#### 1.11.3.16.3. Is Required
False

#### 1.11.3.16.4. Size
255

### 1.11.3.17. createdAt
Timestamp when the request was created.

#### 1.11.3.17.2. Type
DateTime

#### 1.11.3.17.3. Is Required
True

#### 1.11.3.17.4. Default Value
CURRENT_TIMESTAMP

### 1.11.3.18. updatedAt
Timestamp when the request was last updated.

#### 1.11.3.18.2. Type
DateTime

#### 1.11.3.18.3. Is Required
True

#### 1.11.3.18.4. Default Value
CURRENT_TIMESTAMP


### 1.11.4. Primary Keys

- id

### 1.11.5. Unique Constraints


### 1.11.6. Indexes

### 1.11.6.1. idx_aiimagerequest_userid
Index for retrieving requests by user.

#### 1.11.6.1.2. Columns

- userId

#### 1.11.6.1.3. Type
BTree

### 1.11.6.2. idx_aiimagerequest_influencerprofileid
Index for retrieving requests by influencer profile.

#### 1.11.6.2.2. Columns

- influencerProfileId

#### 1.11.6.2.3. Type
BTree

### 1.11.6.3. idx_aiimagerequest_status
Index for filtering requests by status.

#### 1.11.6.3.2. Columns

- status

#### 1.11.6.3.3. Type
BTree

### 1.11.6.4. idx_aiimagerequest_campaignid
Index for retrieving requests linked to a campaign.

#### 1.11.6.4.2. Columns

- campaignId

#### 1.11.6.4.3. Type
BTree

### 1.11.6.5. idx_aiimagerequest_intendeduse
Index for filtering by intended use (e.g., for retention).

#### 1.11.6.5.2. Columns

- intendedUse

#### 1.11.6.5.3. Type
BTree


## 1.12. GeneratedImage
Stores metadata about generated AI images. The binary image data is stored externally. Optimization Note: Indexed by requestId for retrieving images from a request. Hash index supports deduplication/integrity checks. CreatedAt index supports time-based queries and partitioning. RetentionCategory supports retention policy enforcement.

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
Foreign key linking to the AIImageGenerationRequest that produced this image.

#### 1.12.3.2.2. Type
UUID

#### 1.12.3.2.3. Is Required
True

#### 1.12.3.2.4. Is Foreign Key
True

#### 1.12.3.2.5. Constraints

- REFERENCES AIImageGenerationRequest(id) ON DELETE CASCADE

### 1.12.3.3. storageUrl
Secure storage URL or identifier for the actual image file (e.g., Odoo filestore identifier, cloud storage URL). Binary data is stored externally.

#### 1.12.3.3.2. Type
TEXT

#### 1.12.3.3.3. Is Required
True

### 1.12.3.4. fileFormat
File format (e.g., 'png', 'jpeg').

#### 1.12.3.4.2. Type
VARCHAR

#### 1.12.3.4.3. Is Required
True

#### 1.12.3.4.4. Size
10

### 1.12.3.5. fileSize
File size in bytes.

#### 1.12.3.5.2. Type
BIGINT

#### 1.12.3.5.3. Is Required
True

### 1.12.3.6. width
Image width in pixels.

#### 1.12.3.6.2. Type
INT

#### 1.12.3.6.3. Is Required
True

### 1.12.3.7. height
Image height in pixels.

#### 1.12.3.7.2. Type
INT

#### 1.12.3.7.3. Is Required
True

### 1.12.3.8. hashValue
Hash value of the image file (e.g., SHA-256) for integrity verification or deduplication. Nullable if hash calculation fails.

#### 1.12.3.8.2. Type
VARCHAR

#### 1.12.3.8.3. Is Required
False

#### 1.12.3.8.4. Size
64

### 1.12.3.9. retentionCategory
Category determining retention policy (e.g., 'personal_generation', 'campaign_asset_rights_X_years'). Based on request's intendedUse and campaign usage rights.

#### 1.12.3.9.2. Type
VARCHAR

#### 1.12.3.9.3. Is Required
True

#### 1.12.3.9.4. Size
30

### 1.12.3.10. usageRights
Applicable usage rights for this specific image, derived from campaign requirements or platform policy.

#### 1.12.3.10.2. Type
TEXT

#### 1.12.3.10.3. Is Required
False

### 1.12.3.11. createdAt
Timestamp when the image record was created (when generation completed and image stored).

#### 1.12.3.11.2. Type
DateTime

#### 1.12.3.11.3. Is Required
True

#### 1.12.3.11.4. Default Value
CURRENT_TIMESTAMP

### 1.12.3.12. updatedAt
Timestamp when the record was last updated.

#### 1.12.3.12.2. Type
DateTime

#### 1.12.3.12.3. Is Required
True

#### 1.12.3.12.4. Default Value
CURRENT_TIMESTAMP


### 1.12.4. Primary Keys

- id

### 1.12.5. Unique Constraints


### 1.12.6. Indexes

### 1.12.6.1. idx_generatedimage_requestid
Index for retrieving images by generation request.

#### 1.12.6.1.2. Columns

- requestId

#### 1.12.6.1.3. Type
BTree

### 1.12.6.2. idx_generatedimage_hashvalue
Index for finding images by hash value.

#### 1.12.6.2.2. Columns

- hashValue

#### 1.12.6.2.3. Type
BTree

### 1.12.6.3. idx_generatedimage_createdat
Index for time-based queries and partitioning.

#### 1.12.6.3.2. Columns

- createdAt

#### 1.12.6.3.3. Type
BTree

### 1.12.6.4. idx_generatedimage_retentioncategory
Index for filtering images by retention category.

#### 1.12.6.4.2. Columns

- retentionCategory

#### 1.12.6.4.3. Type
BTree


## 1.13. PaymentRecord
Stores influencer payment records. Linked to Odoo accounting module for execution. Optimization Note: Indexed by influencerProfileId and status for managing influencer payouts and tracking status. Indexed by dueDate for payment scheduling.

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
Foreign key linking to the InfluencerProfile. RESTRICT ensures profile is not deleted while pending payments exist.

#### 1.13.3.2.2. Type
UUID

#### 1.13.3.2.3. Is Required
True

#### 1.13.3.2.4. Is Foreign Key
True

#### 1.13.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE RESTRICT

### 1.13.3.3. campaignId
Foreign key linking to the Campaign, if the payment is campaign-specific.

#### 1.13.3.3.2. Type
UUID

#### 1.13.3.3.3. Is Required
False

#### 1.13.3.3.4. Is Foreign Key
True

#### 1.13.3.3.5. Constraints

- REFERENCES Campaign(id) ON DELETE SET NULL

### 1.13.3.4. contentSubmissionId
Foreign key linking to the ContentSubmission, if the payment is based on a specific submission.

#### 1.13.3.4.2. Type
UUID

#### 1.13.3.4.3. Is Required
False

#### 1.13.3.4.4. Is Foreign Key
True

#### 1.13.3.4.5. Constraints

- REFERENCES ContentSubmission(id) ON DELETE SET NULL

### 1.13.3.5. amount
Payment amount.

#### 1.13.3.5.2. Type
DECIMAL

#### 1.13.3.5.3. Is Required
True

#### 1.13.3.5.4. Precision
15

#### 1.13.3.5.5. Scale
2

### 1.13.3.6. currency
Currency code (e.g., 'USD', 'EUR'). ISO 4217 standard.

#### 1.13.3.6.2. Type
VARCHAR

#### 1.13.3.6.3. Is Required
True

#### 1.13.3.6.4. Size
3

### 1.13.3.7. status
Payment status (e.g., 'pending', 'in_progress', 'paid', 'failed'). Indexed for workflow management.

#### 1.13.3.7.2. Type
VARCHAR

#### 1.13.3.7.3. Is Required
True

#### 1.13.3.7.4. Size
20

#### 1.13.3.7.5. Default Value
'pending'

### 1.13.3.8. transactionId
Identifier from the payment gateway or Odoo accounting transaction.

#### 1.13.3.8.2. Type
VARCHAR

#### 1.13.3.8.3. Is Required
False

#### 1.13.3.8.4. Size
50

### 1.13.3.9. paymentMethod
Method of payment (e.g., 'bank_transfer', 'paypal').

#### 1.13.3.9.2. Type
VARCHAR

#### 1.13.3.9.3. Is Required
True

#### 1.13.3.9.4. Size
50

### 1.13.3.10. dueDate
Payment due date. Indexed for scheduling.

#### 1.13.3.10.2. Type
DateTime

#### 1.13.3.10.3. Is Required
False

### 1.13.3.11. paidDate
Date the payment was made.

#### 1.13.3.11.2. Type
DateTime

#### 1.13.3.11.3. Is Required
False

### 1.13.3.12. odooAccountId
Foreign key linking to the corresponding account/journal entry in Odoo's accounting module.

#### 1.13.3.12.2. Type
UUID

#### 1.13.3.12.3. Is Required
False

#### 1.13.3.12.4. Is Foreign Key
True

#### 1.13.3.12.5. Constraints


### 1.13.3.13. createdAt
Timestamp when the payment record was created.

#### 1.13.3.13.2. Type
DateTime

#### 1.13.3.13.3. Is Required
True

#### 1.13.3.13.4. Default Value
CURRENT_TIMESTAMP

### 1.13.3.14. updatedAt
Timestamp when the record was last updated.

#### 1.13.3.14.2. Type
DateTime

#### 1.13.3.14.3. Is Required
True

#### 1.13.3.14.4. Default Value
CURRENT_TIMESTAMP


### 1.13.4. Primary Keys

- id

### 1.13.5. Unique Constraints


### 1.13.6. Indexes

### 1.13.6.1. idx_paymentrecord_influencer_status
Index for finding payments for an influencer by status.

#### 1.13.6.1.2. Columns

- influencerProfileId
- status

#### 1.13.6.1.3. Type
BTree

### 1.13.6.2. idx_paymentrecord_status
Index for filtering all payments by status.

#### 1.13.6.2.2. Columns

- status

#### 1.13.6.2.3. Type
BTree

### 1.13.6.3. idx_paymentrecord_campaignid
Index for finding payments for a campaign.

#### 1.13.6.3.2. Columns

- campaignId

#### 1.13.6.3.3. Type
BTree

### 1.13.6.4. idx_paymentrecord_duedate
Index for finding payments by due date.

#### 1.13.6.4.2. Columns

- dueDate

#### 1.13.6.4.3. Type
BTree


## 1.14. TermsConsent
Stores records of influencer consent to platform Terms of Service and Privacy Policy. Optimization Note: Indexed by influencerProfileId and consentDate (desc) to quickly find the latest consent for an influencer.

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
Foreign key linking to the InfluencerProfile.

#### 1.14.3.2.2. Type
UUID

#### 1.14.3.2.3. Is Required
True

#### 1.14.3.2.4. Is Foreign Key
True

#### 1.14.3.2.5. Constraints

- REFERENCES InfluencerProfile(id) ON DELETE CASCADE

### 1.14.3.3. tosVersion
Version identifier of the Terms of Service agreed to.

#### 1.14.3.3.2. Type
VARCHAR

#### 1.14.3.3.3. Is Required
True

#### 1.14.3.3.4. Size
20

### 1.14.3.4. privacyPolicyVersion
Version identifier of the Privacy Policy agreed to.

#### 1.14.3.4.2. Type
VARCHAR

#### 1.14.3.4.3. Is Required
True

#### 1.14.3.4.4. Size
20

### 1.14.3.5. consentDate
Timestamp when consent was given.

#### 1.14.3.5.2. Type
DateTime

#### 1.14.3.5.3. Is Required
True

#### 1.14.3.5.4. Default Value
CURRENT_TIMESTAMP

### 1.14.3.6. createdAt
Timestamp when the record was created.

#### 1.14.3.6.2. Type
DateTime

#### 1.14.3.6.3. Is Required
True

#### 1.14.3.6.4. Default Value
CURRENT_TIMESTAMP

### 1.14.3.7. updatedAt
Timestamp when the record was last updated (should be same as createdAt unless amended).

#### 1.14.3.7.2. Type
DateTime

#### 1.14.3.7.3. Is Required
True

#### 1.14.3.7.4. Default Value
CURRENT_TIMESTAMP


### 1.14.4. Primary Keys

- id

### 1.14.5. Unique Constraints


### 1.14.6. Indexes

### 1.14.6.1. idx_termsconsent_influencer_consentdate
Composite index for finding the latest consent record for an influencer.

#### 1.14.6.1.2. Columns

- influencerProfileId
- consentDate DESC

#### 1.14.6.1.3. Type
BTree


## 1.15. AuditLog
Stores system audit trail records. Optimization Note: Implement range partitioning on this table using the 'timestamp' column (e.g., monthly or quarterly partitions) for high volume. Indexed by timestamp, event type, and target entity/id for efficient searching.

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

### 1.15.3.2. timestamp
Timestamp of the audited event (UTC). Indexed and suitable for partitioning.

#### 1.15.3.2.2. Type
DateTime

#### 1.15.3.2.3. Is Required
True

#### 1.15.3.2.4. Default Value
CURRENT_TIMESTAMP

### 1.15.3.3. eventType
Category of the event (e.g., 'user_login', 'kyc_update', 'campaign_status_change', 'image_generate'). Indexed for filtering.

#### 1.15.3.3.2. Type
VARCHAR

#### 1.15.3.3.3. Is Required
True

#### 1.15.3.3.4. Size
50

### 1.15.3.4. actorUserId
Foreign key linking to the Odoo user who performed the action (actor). Nullable if action is system-initiated.

#### 1.15.3.4.2. Type
UUID

#### 1.15.3.4.3. Is Required
False

#### 1.15.3.4.4. Is Foreign Key
True

#### 1.15.3.4.5. Constraints

- REFERENCES res_users(id) ON DELETE SET NULL

### 1.15.3.5. targetEntity
Name of the entity/model affected (e.g., 'InfluencerProfile', 'Campaign'). Indexed with targetId.

#### 1.15.3.5.2. Type
VARCHAR

#### 1.15.3.5.3. Is Required
True

#### 1.15.3.5.4. Size
50

### 1.15.3.6. targetId
ID of the specific record affected. Nullable if the action doesn't apply to a specific record (e.g., 'user_login'). Indexed with targetEntity.

#### 1.15.3.6.2. Type
UUID

#### 1.15.3.6.3. Is Required
False

### 1.15.3.7. action
Specific action performed (e.g., 'create', 'update', 'delete', 'view', 'approve', 'reject').

#### 1.15.3.7.2. Type
VARCHAR

#### 1.15.3.7.3. Is Required
True

#### 1.15.3.7.4. Size
20

### 1.15.3.8. details
JSON or JSONB field containing additional details about the event (e.g., old/new values for updates).

#### 1.15.3.8.2. Type
JSON

#### 1.15.3.8.3. Is Required
False

### 1.15.3.9. ipAddress
IP address from which the action originated.

#### 1.15.3.9.2. Type
VARCHAR

#### 1.15.3.9.3. Is Required
False

#### 1.15.3.9.4. Size
45


### 1.15.4. Primary Keys

- id

### 1.15.5. Unique Constraints


### 1.15.6. Indexes

### 1.15.6.1. idx_auditlog_timestamp
Index for time-based queries on audit logs.

#### 1.15.6.1.2. Columns

- timestamp

#### 1.15.6.1.3. Type
BTree

### 1.15.6.2. idx_auditlog_eventtype
Index for filtering audit logs by event type.

#### 1.15.6.2.2. Columns

- eventType

#### 1.15.6.2.3. Type
BTree

### 1.15.6.3. idx_auditlog_targetentity_targetid
Composite index for finding audit logs related to a specific entity record.

#### 1.15.6.3.2. Columns

- targetEntity
- targetId

#### 1.15.6.3.3. Type
BTree

### 1.15.6.4. idx_auditlog_actoruserid
Index for filtering audit logs by the user who performed the action.

#### 1.15.6.4.2. Columns

- actorUserId

#### 1.15.6.4.3. Type
BTree


## 1.16. CampaignPerformanceMV
Materialized View: Pre-aggregates campaign performance metrics based on Campaign and CampaignApplication data. Refreshed periodically (scheduled cron job). Optimization Note: Use read replicas for serving dashboard data derived from this view.

### 1.16.3. Attributes

### 1.16.3.1. campaignId
Foreign key linking to the Campaign.

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
Denormalized campaign name for convenience.

#### 1.16.3.2.2. Type
VARCHAR

#### 1.16.3.2.3. Is Required
True

#### 1.16.3.2.4. Size
100

### 1.16.3.3. totalApplications
Total number of applications received for the campaign.

#### 1.16.3.3.2. Type
INT

#### 1.16.3.3.3. Is Required
True

#### 1.16.3.3.4. Default Value
0

### 1.16.3.4. approvedApplications
Number of applications approved for the campaign.

#### 1.16.3.4.2. Type
INT

#### 1.16.3.4.3. Is Required
True

#### 1.16.3.4.4. Default Value
0

### 1.16.3.5. totalSubmissions
Total number of content submissions for the campaign.

#### 1.16.3.5.2. Type
INT

#### 1.16.3.5.3. Is Required
True

#### 1.16.3.5.4. Default Value
0

### 1.16.3.6. approvedSubmissions
Number of content submissions approved for the campaign.

#### 1.16.3.6.2. Type
INT

#### 1.16.3.6.3. Is Required
True

#### 1.16.3.6.4. Default Value
0

### 1.16.3.7. totalEngagement
Aggregated engagement metric (e.g., sum of likes, shares, etc., if captured).

#### 1.16.3.7.2. Type
BIGINT

#### 1.16.3.7.3. Is Required
False

#### 1.16.3.7.4. Default Value
0

### 1.16.3.8. lastRefreshedAt
Timestamp when the materialized view was last refreshed.

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


## 1.17. PlatformSetting
Stores platform-wide configuration settings. Optimization Note: This table is expected to be small and frequently accessed; cache settings in application memory.

### 1.17.3. Attributes

### 1.17.3.1. id
#### 1.17.3.1.2. Type
UUID

#### 1.17.3.1.3. Is Required
True

#### 1.17.3.1.4. Is Primary Key
True

#### 1.17.3.1.5. Is Unique
True

#### 1.17.3.1.6. Default Value
gen_random_uuid()

### 1.17.3.2. key
Unique key for the setting (e.g., 'kyc_manual_review_required', 'ai_image_quota_default').

#### 1.17.3.2.2. Type
VARCHAR

#### 1.17.3.2.3. Is Required
True

#### 1.17.3.2.4. Is Unique
True

#### 1.17.3.2.5. Size
100

### 1.17.3.3. value
The value of the setting (can be boolean, string, number, or JSON).

#### 1.17.3.3.2. Type
TEXT

#### 1.17.3.3.3. Is Required
False

### 1.17.3.4. dataType
Data type of the value ('string', 'integer', 'decimal', 'boolean', 'json').

#### 1.17.3.4.2. Type
VARCHAR

#### 1.17.3.4.3. Is Required
True

#### 1.17.3.4.4. Size
20

### 1.17.3.5. description
Description of the setting and its purpose.

#### 1.17.3.5.2. Type
TEXT

#### 1.17.3.5.3. Is Required
False


### 1.17.4. Primary Keys

- id

### 1.17.5. Unique Constraints

### 1.17.5.1. uq_platformsetting_key
Ensures setting keys are unique.

#### 1.17.5.1.2. Columns

- key


### 1.17.6. Indexes




---

# 2. Diagrams

- **Diagram_Title:** Influencer & Account Management  
**Diagram_Area:** User Profiles, Account Verification, Areas of Expertise, Audit Trail  
**Explanation:** This diagram illustrates the core influencer profile linked to the Odoo user. It includes associated data like social media accounts, KYC details, bank information, terms consent, and areas of influence (via a join table). It also shows links to the audit log.  
**Mermaid_Text:** erDiagram
    res_users {
        UUID id PK
    }
    InfluencerProfile {
        UUID id PK
        UUID userId FK
    }
    SocialMediaProfile {
        UUID id PK
        UUID influencerProfileId FK
    }
    KYCData {
        UUID id PK
        UUID influencerProfileId FK
        UUID reviewerUserId FK
    }
    BankAccount {
        UUID id PK
        UUID influencerProfileId FK
    }
    TermsConsent {
        UUID id PK
        UUID influencerProfileId FK
    }
    AreaOfInfluence {
        UUID id PK
    }
    InfluencerAreaOfInfluence {
        UUID influencerProfileId PK
        UUID areaOfInfluenceId PK
    }
    AuditLog {
        UUID id PK
        UUID actorUserId FK
    }

    InfluencerProfile ||--|| res_users : "linked to" userId
    InfluencerProfile ||--o{ SocialMediaProfile : "has" socialMedia
    InfluencerProfile ||--o{ KYCData : "submits" kycData
    InfluencerProfile ||--o{ BankAccount : "has" bankAccount
    InfluencerProfile ||--o{ TermsConsent : "agrees to" termsConsent
    res_users }|--o{ KYCData : "reviewed by" reviewerUserId
    InfluencerProfile }o--{ InfluencerAreaOfInfluence : "categorized by" influencerProfileId
    AreaOfInfluence }o--{ InfluencerAreaOfInfluence : "used in" areaOfInfluenceId
    res_users }|--o{ AuditLog : "acted by" actorUserId  
- **Diagram_Title:** Campaign & Content Workflow  
**Diagram_Area:** Campaign Lifecycle, Application Process, Content Submission & Review, Performance Metrics  
**Explanation:** This diagram focuses on the campaign process. It shows how campaigns receive influencer applications (M:M relationship), which lead to content submissions. Submissions are reviewed and can link to AI-generated images. Campaign performance is tracked via a materialized view. Includes links to influencers and reviewers.  
**Mermaid_Text:** erDiagram
    Campaign {
        UUID id PK
    }
    CampaignApplication {
        UUID id PK
        UUID campaignId FK
        UUID influencerProfileId FK
        UUID reviewerUserId FK
    }
    ContentSubmission {
        UUID id PK
        UUID campaignApplicationId FK
        UUID generatedImageId FK
        UUID reviewedByUserId FK
    }
    CampaignPerformanceMV {
        UUID campaignId PK
    }
    InfluencerProfile {
        UUID id PK
    }
    res_users {
        UUID id PK
    }
    GeneratedImage {
        UUID id PK
    }

    Campaign }o--{ CampaignApplication : "receives" application
    InfluencerProfile }o--{ CampaignApplication : "applies to" application
    res_users }|--o{ CampaignApplication : "reviewed by" reviewerUserId
    CampaignApplication ||--o{ ContentSubmission : "includes" submission
    res_users }|--o{ ContentSubmission : "reviewed by" reviewedByUserId
    GeneratedImage }|--o{ ContentSubmission : "uses" generatedImageId
    Campaign ||--|| CampaignPerformanceMV : "tracks" performance  
- **Diagram_Title:** AI Image Generation & Payments  
**Diagram_Area:** AI Workflow, Image Storage, Financial Transactions  
**Explanation:** This diagram details the AI image generation process, linking models, requests, and the resulting generated images. It also illustrates the payment system, showing how payment records are associated with influencers, campaigns, or specific content submissions. Includes links to the requesting user.  
**Mermaid_Text:** erDiagram
    AIImageModel {
        UUID id PK
    }
    AIImageGenerationRequest {
        UUID id PK
        UUID userId FK
        UUID influencerProfileId FK
        UUID campaignId FK
        UUID modelId FK
    }
    GeneratedImage {
        UUID id PK
        UUID requestId FK
    }
    PaymentRecord {
        UUID id PK
        UUID influencerProfileId FK
        UUID campaignId FK
        UUID contentSubmissionId FK
    }
    InfluencerProfile {
        UUID id PK
    }
    res_users {
        UUID id PK
    }
    Campaign {
        UUID id PK
    }
    ContentSubmission {
        UUID id PK
    }

    AIImageModel ||--o{ AIImageGenerationRequest : "uses" modelId
    res_users ||--o{ AIImageGenerationRequest : "requested by" userId
    InfluencerProfile ||--o{ AIImageGenerationRequest : "for profile" influencerProfileId
    Campaign }|--o{ AIImageGenerationRequest : "for campaign" campaignId
    AIImageGenerationRequest ||--o{ GeneratedImage : "produces" image
    InfluencerProfile ||--o{ PaymentRecord : "paid to" influencerProfileId
    Campaign }|--o{ PaymentRecord : "for campaign" campaignId
    ContentSubmission }|--o{ PaymentRecord : "for content" contentSubmissionId  
- **Diagram_Title:** Platform Settings  
**Diagram_Area:** System Configuration  
**Explanation:** A simple table for storing platform-wide configuration keys and values.  
**Mermaid_Text:** erDiagram
    PlatformSetting {
        UUID id PK
        VARCHAR key
        TEXT value
    }  


---

