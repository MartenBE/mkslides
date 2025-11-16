<!--
SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)

SPDX-License-Identifier: MIT
-->

# Strict

---

## Relative links in same folder

[](someslides-2.md)
[](./someslides-2.md)
[test](someslides-2.md)
[test](./someslides-2.md)

<a href="someslides-2.md">test</a>
<a href="./someslides-2.md">test</a>
<a target="_blank" href="someslides-2.md" class="dummy">test</a>
<a target="_blank" href="./someslides-2.md" class="dummy">test</a>

---

## Relative links in other folder

[](category-1/someslides-3.md)
[](./category-1/someslides-3.md)
[test](category-1/someslides-3.md)
[test](./category-1/someslides-3.md)

<a href="category-1/someslides-3.md">test</a>
<a href="./category-1/someslides-3.md">test</a>
<a target="_blank" href="category-1/someslides-3.md" class="dummy">test</a>
<a target="_blank" href="./category-1/someslides-3.md" class="dummy">test</a>

---

## Public URLs

[](https://example.com/test.md)
[test](https://example.com/test.md)

<a href="https://example.com/test.md">test</a>
<a target="_blank" href="https://example.com/test.md" class="dummy">test</a>

---

## Absolute links in other folder

[](/folder/test.md)
[test](/folder/test.md)

<a href="/folder/test.md">test</a>
<a target="_blank" href="/folder/test.md" class="dummy">test</a>

---

<!-- # Not existing link

This should throw when using `-s`:

[test](./some-random-md-link)

--- -->
