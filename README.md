# Salesforce Profile Cleaner

Cleans a Salesforce profile (or profiles) of all elements for which it has no access, so they're just takin' up space, and mucking up deployments, especially in the case of a partial org migration where your org won't have all the referenced metadata.

## Note Uno
Retrieving a Salesforce profile only brings with it references to the metadata that was retrieved at the same time. It's dumb and annoying (though sometimes, handy). The *Salesforce Profile Cleaner* will remove irrelevant elements that are in your current local version of the file. The original file will **not** be altered; a copy will be made with the same name, appended by `__CLEANED`.

## Note Dos
The *Salesforce Profile Cleaner* won't take a hammer to your profile and delete any old **false** element. For example, it will delete field permissions only if the `readable` property is **false**. If `readable` is **true** but `editable` is **false**, it'll ignore it. So, chillax!

## Prerequisites
- Python (https://www.python.org/downloads/)
- Minimal command line know-how

## Usage
`python profile_cleaner.py [path_to_profile]`
`python profile_cleaner.py [path_to_profiles_folder]`

**Returns** `[path_to_profile]__CLEANED`

## Example

`python profile_cleaner.py MySalesforceProjects/AwesomeSauce/force-app/main/default/profiles/Baconator.profile-meta.xml`

**Returns** `MySalesforceProjects/AwesomeSauce/force-app/main/default/profiles/Baconator.profile-meta.xml__CLEANED`
