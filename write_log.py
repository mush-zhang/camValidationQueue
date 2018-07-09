"""
This file will be used for recording log messages when:
1. There is more than 1 cameras in the db with the same retrieval method.
   This signals a problem in the db. The camera information shold be recorded.
2. There is one camera with the same retrieval method when new camera adds,
   but the information of the new camera is not exactly the same with the older one,
"""