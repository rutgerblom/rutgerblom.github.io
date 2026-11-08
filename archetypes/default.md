+++
date = '{{ .Date }}'
draft = true
slug = '{{ .File.ContentBaseName | anchorize }}'
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
+++
