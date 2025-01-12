# Some slides

---

## Lorem ipsum

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---

## Alfabet

-   A
-   B
-   C
-   D
-   E

---

## Markdown images - local

![](./img/example-1.png)

---

## Markdown images - public URL

![](https://example.org/example-1.png)

---

## HTML img tag images - local

<img src="./img/example-2.png" />

---

## HTML img tag images - public URL

<img src="https://example.org/example-2.png" />

---

## Background images - local

<!-- .slide: data-background-image="./img/example-3.png" -->

---

## Background images - public URL

<!-- .slide: data-background-image="https://example.org/example-3.png" -->

---

## Link to local file

[](./test-1.txt)
[](test-2.txt)

---

## Escape using `<` and `>`

![](<./img/example-(7).png>)
![](<https://example.org/example_(1).png>)
[](<./test-(3).txt>)
[](<https://example.org/example_(2).html>)

---

## Using emoji's

:warning:
:thumbsup: <!-- checking aliases https://www.webfx.com/tools/emoji-cheat-sheet/ -->

---

## Don't try to parse anchor links

This should not throw an error:

[Go to anchor](#some-random-anchor)

---

## Don't try to parse links in code blocks

This should not throw an error:

`[test](./some-random-md-link)`
`![test](./some-random-md-image.png)`
`<a href="./some-random-html-link">test</a>`
`<img src="./some-random-html-image.png" />`

```markdown
[test](./some-random-md-link)
![test](./some-random-md-image.png)
```

```html
<a href="./some-random-html-link">test</a>
<img src="./some-random-html-image.png" />
```

    [test](./some-random-md-link)
    ![test](./some-random-md-image.png)
    <a href="./some-random-html-link">test</a>
    <img src="./some-random-html-image.png" />

<!--
[test](./some-random-md-link)
![test](./some-random-md-image.png)
<a href="./some-random-html-link">test</a>
<img src="./some-random-html-image.png" />
-->

```md
<!--
    [test](./some-random-md-link)
    ![test](./some-random-md-image.png)
-->
```

    <!--
        [test](./some-random-md-link)
        ![test](./some-random-md-image.png)
    -->

```html
<!--
    <a href="./some-random-html-link">test</a>
    <img src="./some-random-html-image.png" />
-->
<!-- .slide: data-background-image="./some-random-background-image.png" -->
```

    <!--
        <a href="./some-random-html-link">test</a>
        <img src="./some-random-html-image.png" />
    -->
    <!-- .slide: data-background-image="./some-random-background-image.png" -->

---

## Preprocessing

@@@@@-@@@@
@@@-@@
@

---

## Video

<video controls preload="metadata">
    <source src="./video/demo.webm" type="video/webm"/>
    Video not supported.
</video>

---
