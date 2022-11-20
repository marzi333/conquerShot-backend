import csv
import shutil
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--split',type=str,default='train')
  args = parser.parse_args()

  split = args.split
  if split == 'train' or split == 'val':
    csv_name = 'label'
  else:
    csv_name = split

  with open(f"./HackaTUM_Data/dataset/hackatum_dataset/{split}/{csv_name}.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      if row[4] == 'highway':
          continue
      else:
          img_path = f"./HackaTUM_Data/dataset/hackatum_dataset/{split}/{row[0]}.jpg"
          shutil.copy(img_path,f'./huawei_dataset/{split}/{row[4]}/')