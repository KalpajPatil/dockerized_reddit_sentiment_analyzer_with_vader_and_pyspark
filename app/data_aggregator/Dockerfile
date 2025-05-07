FROM python

USER root

WORKDIR /app

COPY /app/data_aggregator/excel_generator.py /app/

RUN mkdir -p /excel_output/output_data /final_csv

RUN apt-get update && apt-get install -y python3-pip && \
        pip3 install pandas openpyxl numpy

RUN chmod +x /app/excel_generator.py

RUN chmod -R 777 /excel_output/output_data /final_csv

CMD [ "python", "excel_generator.py" ]

USER 1001