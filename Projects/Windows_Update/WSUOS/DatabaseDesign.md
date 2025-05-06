# Database Design for Windows Update OS

# Use case

1. User can find details information about Windows Update.
   - Data include bundle Id, title, creation date, DeploymentAction, isBundle, isLeaf, revision Id, KB, and more.
2. User can search for specific updates.
   - Search by KB, update Id or revision Id.


## Tables

### Files
   - Contains information about the files in the update.
Attributes:

| Attribute | Type | Key         |
| --------- | ---- | ----------- |
| `id`      | TEXT | PRIMARY KEY |
| `Url`     | TEXT |

### Update_Metadata

Attributes:

| Attribute          | Type | Key         |
| ------------------ | ---- | ----------- |
| `id`               | TEXT | PRIMARY KEY |
| `CreationDate`     | TEXT |
| `RevisionId`       | TEXT |
| `RevisionNumber`   | TEXT |
| `DefaultLanguage`  | TEXT |
| `IsLeaf`           | TEXT |
| `IsBundle`         | TEXT |
| `DeploymentAction` | TEXT |
| `prerequisites`    | TEXT |
| `languages`        | TEXT |

### Update_details

Attributes:

| Attribute            | Type | Key         |
| -------------------- | ---- | ----------- |
| `id`                 | TEXT | PRIMARY KEY |
| `file_id`            | TEXT |
| `bundle_id`          | TEXT |
| `Properties`         | TEXT |
| `Relationships`      | TEXT |
| `ApplicabilityRules` | TEXT |



### Update_KB_info

Attributes:

| Attribute       | Type | Key         |
| --------------- | ---- | ----------- |
| `id`            | TEXT | PRIMARY KEY |
| `KB`            | TEXT |
| `Title`         | TEXT |
| `Architectures` | TEXT |
| `Categories`    | TEXT |
| `OS`            | TEXT |