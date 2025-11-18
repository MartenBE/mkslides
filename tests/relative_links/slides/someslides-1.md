<!--
SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)

SPDX-License-Identifier: MIT
-->

# Relative links

---

## Existing relative links

[](test-1)
[](./test-1)
[](some-folder/test-4)
[](./some-folder/test-4)

<!-- prettier-ignore-start -->
[](<test-1>)
[](<./test-1>)
[](<some-folder/test-4>)
[](<./some-folder/test-4>)
<!-- prettier-ignore-end -->

[](test-2.txt)
[](./test-2.txt)
[](some-folder/test-5.txt)
[](./some-folder/test-5.txt)

<!-- prettier-ignore-start -->
[](<test-2.txt>)
[](<./test-2.txt>)
[](<some-folder/test-5.txt>)
[](<./some-folder/test-5.txt>)
<!-- prettier-ignore-end -->

![](test-3.png)
![](./test-3.png)
![](some-folder/test-6.png)
![](./some-folder/test-6.png)

<!-- prettier-ignore-start -->
![](<test-3.png>)
![](<./test-3.png>)
![](<some-folder/test-6.png>)
![](<./some-folder/test-6.png>)
<!-- prettier-ignore-end -->

<a href="test-1">test</a>
<a href="./test-1">test</a>
<a href="some-folder/test-4">test-4</a>
<a href="./some-folder/test-4">test-4</a>

<a href="test-2.txt">test-2</a>
<a href="./test-2.txt">test-2</a>
<a href="some-folder/test-5.txt">test-5</a>
<a href="./some-folder/test-5.txt">test-5</a>

<img src="test-3.png" />
<img src="./test-3.png" />
<img src="some-folder/test-6.png" />
<img src="./some-folder/test-6.png" />

---

## Absolute links

Absolute links are not checked.

[](/some-absolute-folder/some-absolute-file)
[](/some-absolute-folder/some-absolute-file.txt)
![](/some-absolute-folder/some-absolute-file.png)

<!-- prettier-ignore-start -->
[](</some-absolute-folder/some-absolute-file>)
[](</some-absolute-folder/some-absolute-file.txt>)
![](</some-absolute-folder/some-absolute-file.png>)
<!-- prettier-ignore-end -->

<a href="/some-absolute-folder/some-absolute-file.txt">test</a>

<img src="/some-absolute-folder/some-absolute-file.png" />

---

## URLs

URLs are not checked.

[](https://example.com/some-file)
[](https://example.com/some-file.txt)
![](https://example.com/some-file.png)

<!-- prettier-ignore-start -->
[](<https://example.com/some-file>)
[](<https://example.com/some-file.txt>)
![](<https://example.com/some-file.png>)
<!-- prettier-ignore-end -->

<a href="https://example.com/some-file.txt">test</a>

<img src="https://example.com/some-file.png" />

---

## Non existing links in comments

Commented out links are not checked.

<!--
[](some-non-existing-file)
[](./some-non-existing-file)

[](<some-non-existing-file>)
[](<./some-non-existing-file>)

![](some-non-existing-file.txt)
![](./some-non-existing-file.txt)

![](<some-non-existing-file.txt>)
![](<./some-non-existing-file.txt>)

![](some-non-existing-file.png)
![](./some-non-existing-file.png)

![](<some-non-existing-file.png>)
![](<./some-non-existing-file.png>)

<a href="some-non-existing-file">test</a>
<a href="./some-non-existing-file">test</a>

<a href="some-non-existing-file.txt">test</a>
<a href="./some-non-existing-file.txt">test</a>

<img src="some-non-existing-file.png" />
<img src="./some-non-existing-file.png" />
-->

---

## Non existing links in code blocks

Links in code blocks are not checked.

```md
[](some-non-existing-file)
[](./some-non-existing-file)

<!-- prettier-ignore-start -->
[](<some-non-existing-file>)
[](<./some-non-existing-file>)
<!-- prettier-ignore-end -->

![](some-non-existing-file.txt)
![](./some-non-existing-file.txt)

<!-- prettier-ignore-start -->
![](<some-non-existing-file.txt>)
![](<./some-non-existing-file.txt>)
<!-- prettier-ignore-end -->

![](some-non-existing-file.png)
![](./some-non-existing-file.png)

<!-- prettier-ignore-start -->
![](<some-non-existing-file.png>)
![](<./some-non-existing-file.png>)
<!-- prettier-ignore-end -->

<a href="some-non-existing-file">test</a>
<a href="./some-non-existing-file">test</a>

<a href="some-non-existing-file.txt">test</a>
<a href="./some-non-existing-file.txt">test</a>

<img src="some-non-existing-file.png" />
<img src="./some-non-existing-file.png" />
```

    [](some-non-existing-file)
    [](./some-non-existing-file)

    [](<some-non-existing-file>)
    [](<./some-non-existing-file>)

    ![](some-non-existing-file.txt)
    ![](./some-non-existing-file.txt)

    ![](<some-non-existing-file.txt>)
    ![](<./some-non-existing-file.txt>)

    ![](some-non-existing-file.png)
    ![](./some-non-existing-file.png)

    ![](<some-non-existing-file.png>)
    ![](<./some-non-existing-file.png>)

    <a href="some-non-existing-file">test</a>
    <a href="./some-non-existing-file">test</a>

    <a href="some-non-existing-file.txt">test</a>
    <a href="./some-non-existing-file.txt">test</a>

    <img src="some-non-existing-file.png" />
    <img src="./some-non-existing-file.png" />

---
