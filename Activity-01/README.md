This project is a Python-based tool designed to recursively scan directories for files, displaying their relative paths and sizes in kilobytes. The project includes two scripts: setup_files.py and scan.py. The setup_files.py script generates a test directory structure with subfolders and .txt files, providing a realistic environment for testing. The scan.py script performs the scanning operation, featuring several enhancements:

Minimum Size Filter - The --min-size option filters files to display only those larger than the specified size in kilobytes. For example, running py scan.py test_root --min-size 0.1 displays files larger than 0.1 KB.

Folder Summary - At the end of the output, the script provides a summary of the number of files and their total size grouped by folder.

CSV Output - Scanned results can be exported to a CSV file named output.csv with details of each file.

Custom File Extensions - The --ext option allows scanning for any file extension, not just .txt, enabling greater flexibility.

To use the project, run setup_files.py to create the directory structure, and then execute scan.py with the desired options. This project demonstrates foundational scripting skills for navigating, filtering, and processing nested directories, making it a practical introduction to automation tasks.

File                                      Size (KB) 
----------------------------------------------------
docs\file0.txt                                  0.1 
docs\file1.txt                                  0.1 
docs\file2.txt                                  0.1 
docs\file3.txt                                  0.1 
docs\file4.txt                                  0.1 
logs\file0.txt                                  0.1 
logs\file1.txt                                  0.1 
logs\file2.txt                                  0.1 
logs\file3.txt                                  0.1
logs\file4.txt                                  0.1 
docs\subfolder\file0.txt                        0.1 
docs\subfolder\file1.txt                        0.1 
docs\subfolder\file2.txt                        0.1 
docs\subfolder\file3.txt                        0.1 
docs\subfolder\file4.txt                        0.1 
logs\archive\file0.txt                          0.1 
logs\archive\file1.txt                          0.1 
logs\archive\file2.txt                          0.1 
logs\archive\file3.txt                          0.1 
logs\archive\file4.txt                          0.1 
----------------------------------------------------
Displayed files: 20
Total size: 2.0 KB