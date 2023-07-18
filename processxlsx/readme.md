##读写excel文件，格式为xxx.xlsx
需要先安装openyxl
pip install  openpyxl 

1.加载xlsx文件
workbook = load_workbook('/test.xlsx')
2.选择第一个工作表
worksheet = workbook.worksheets[0]
3.遍历每一行
for row_number, row in enumerate(worksheet.iter_rows(min_row=2), start=2):
    # 4.获取待处理数据，获取每行第5列的数据
    query = row[4].value #从0开始计数
    print("query is ",query)
    ##具体处理，得到结果

    print("生成的答案:", answer)
    print("time is ",response_time)
    # 5.写入，将得到的结果写入每行的第8列，时间写入每行的第9列
    cell = worksheet.cell(row=row_number, column=8) 
    cell.value = answer
    cell = worksheet.cell(row=row_number, column=9)##这种方式列的索引从1开始
    cell.value = response_time
5.写入xlsx文件
workbook.save('/test.xlsx')

