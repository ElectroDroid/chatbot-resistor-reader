#!/usr/bin/env python

import sys

sitepackage = "D:\home\site\wwwroot\libs"

#sitepackage = "..\libs"
sys.path.append(sitepackage)

result = sys.argv[1]
cv_version = cv2.__version__

print cv_version