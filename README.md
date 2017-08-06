# car-complaints-text-analytics
A sample text analytics project. The input data being a set of car complaints and analysis is done to get the complaint area.

Requirement
-------------
python 2

Execution
-----------
python text_analytics.py

Input
-------
Must have a csv file with list of complaints regarding cars.
User must enter the full path of the CSV file and the colom to be analyzed.

Output
-------
A newly added colom with in the file with the complaint area identified.

Customization
----------------
Add /  delete / edit words or list of words in the check_list.py file.

Changes to be made
------------------------
Only one colom will be analyzed now which should be changed to accept the number of coloms as user choice.
The analytics is too specific to car complaints - Need to make it generic to accomodate other stream complaints too.
Need to make better use of the new words identifed during the process based on the frequency of their occurence.
