<!--
SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)

SPDX-License-Identifier: MIT
-->

# Some slides

---

## Markdown images - local

![](img/example-1.png)
![](./img/example-1.png)
![](somefolder/example-2.png)
![](./somefolder/example-2.png)
![](img/somefolder/example-3.png)
![](./img/somefolder/example-3.png)
![](example-4.png)
![](./example-4.png)

<!-- prettier-ignore-start -->
![](<img/example-1.png>)
![](<./img/example-1.png>)
![](<somefolder/example-2.png>)
![](<./somefolder/example-2.png>)
![](<img/somefolder/example-3.png>)
![](<./img/somefolder/example-3.png>)
![](<example-4.png>)
![](<./example-4.png>)
<!-- prettier-ignore-end -->

---

## Markdown images - public URL

![](https://example.org/example-1.png)

<!-- prettier-ignore -->
![](<https://example.org/example-1.png>)

---

## HTML img tag images - local

<img src="./img/example-1.png" />

---

## HTML img tag images - public URL

<img src="https://example.org/example-1.png" />

---

## Background images - local

<!-- .slide: data-background-image="./img/example-1.png" -->

---

## Background images - public URL

<!-- .slide: data-background-image="https://example.org/example-1.png" -->
