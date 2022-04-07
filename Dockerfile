FROM python:3.8.13-slim
LABEL project zenjob-challenge
ENV ENV=''
ENV ACCESS_KEY_ID=''
ENV SECRET_ACCESS_KEY=''
ARG UNAME=zenu
RUN useradd -ms /bin/bash $UNAME
WORKDIR /home/$UNAME
RUN mkdir .aws \
    && pip install boto3
COPY aws/credential.tmpl .aws/credential.tmpl
COPY utils/upload_file_s3.py ./upload_file_s3.py
RUN chown -R $UNAME:$UNAME upload_file_s3.py  .aws/
USER $UNAME
# Run the command on container startup
CMD ["python", "upload_file_s3.py"]