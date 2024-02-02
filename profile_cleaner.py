import sys
import re
import os
import xml.etree.ElementTree as ET

def namespace(element):
	return re.match(r'\{.*\}', element.tag).group(0)

def main():
	if len(sys.argv) != 2:
		return None

	try:
		clean_profile(sys.argv[1])
	except IsADirectoryError:
		for(root, dirs, files) in os.walk(sys.argv[1]):
			for f in files:
				try:
					print(root + f, 23)
					clean_profile(root + f)
				except Exception as e:
					print(e)

def clean_profile(p):
	tree = ET.parse(p)
	root = tree.getroot()
	ns = namespace(root)
	ET.register_namespace('', ns[1:-1])

	with open(p + '__CLEANED', 'w', encoding='UTF-8') as f:
		removedObjects = []
		removedRecordTypes = []

		for application in root.findall(ns + 'applicationVisibilities'):
			visible = application.find(ns + 'visible')
			if (visible.text == 'false'):
				root.remove(application)

		for apexClass in root.findall(ns + 'classAccesses'):
			enabled = apexClass.find(ns + 'enabled')
			if (enabled.text == 'false'):
				root.remove(apexClass)

		for externalDataSource in root.findall(ns + 'externalDataSourceAccesses'):
			enabled = externalDataSource.find(ns + 'enabled')
			if (enabled.text == 'false'):
				root.remove(externalDataSource)

		for field in root.findall(ns + 'fieldPermissions'):
			readable = field.find(ns + 'readable')
			if (readable.text == 'false'):
				root.remove(field)

		for flow in root.findall(ns + 'flowAccesses'):
			enabled = flow.find(ns + 'enabled')
			if (enabled.text == 'false'):
				root.remove(flow)

		for object in root.findall(ns + 'objectPermissions'):
			allowRead = object.find(ns + 'allowRead')
			if (allowRead.text == 'false'):
				root.remove(object)
				removedObjects.append(object.find(ns + 'object').text)

		for apexPage in root.findall(ns + 'pageAccesses'):
			enabled = apexPage.find(ns + 'enabled')
			if (enabled.text == 'false'):
				root.remove(apexPage)

		for recordType in root.findall(ns + 'recordTypeVisibilities'):
			visible = recordType.find(ns + 'visible')
			if (visible.text == 'false'):
				root.remove(recordType)
				removedRecordTypes.append(recordType.find(ns + 'recordType').text)

		for tab in root.findall(ns + 'tabVisibilities'):
			visibility = tab.find(ns + 'visibility')
			if (visibility.text == 'Hidden'):
				root.remove(tab)

		for layout in root.findall(ns + 'layoutAssignments'):
			recordType = layout.find(ns + 'recordType')
			if (recordType is None and layout.find(ns + 'layout').text.partition('-')[0] in removedObjects):
				root.remove(layout)
			elif (recordType is not None and recordType.text in removedRecordTypes):
				root.remove(layout)

		tree.write(p + '__CLEANED', encoding='utf-8', xml_declaration=True)
		print(p)

if __name__ == '__main__':
	main()