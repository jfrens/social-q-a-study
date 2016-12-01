#! python2
import os
from boto.mturk.connection import MTurkConnection
from boto.mturk.connection import ExternalQuestion
from boto.mturk.price import Price

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

HOST = 'mechanicalturk.sandbox.amazonaws.com'

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, host = HOST)

url = "https://127.0.0.1"
title = "Rate the quality of this answer"
description = "Please read the instructions and then rate the quality of the answer. This task should take approximately 30 seconds"
keywords = ["rate", "answer"]
frame_height = 800
amount = 0.05

questionform = ExternalQuestion(url, frame_height)

create_hit_result = connection.create_hit(
            title=title,
            description=description,
            keywords=keywords,
            max_assignments=1,
            question=questionform,
            reward=Price(amount=amount),
            response_groups=('Minimal', 'HITDetail')
        )

