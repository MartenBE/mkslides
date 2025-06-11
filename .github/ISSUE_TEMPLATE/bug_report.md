---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''
---

:warning: First, test if the bug isn't related by [reveal.js (upstream)](https://github.com/hakimel/reveal.js/). See if you can reproduce the bug in the snippet below:

```html
<html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@latest/dist/reset.min.css" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@latest/dist/reveal.min.css " />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@latest/dist/theme/white.min.css" />

        <script src="https://cdn.jsdelivr.net/npm/reveal.js@latest/dist/reveal.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/reveal.js@latest/plugin/markdown/markdown.min.js"></script>
    </head>
    <body>
        <div class="reveal">
            <div class="slides">
                <section data-markdown>
                    <textarea data-template>

                        # Title page

                        ---

                        ## Slide 1

                        A paragraph with some text and a [link](https://google.com).

                        ---
                        ## Slide 2

                        A list:

                        - Item 1
                        - Item 2
                        - Item 3

                        ---

                        ## Slide 3

                        Some more text.

                        ---

                    </textarea>
                </section>
            </div>
        </div>

        <script>
            Reveal.initialize({
                plugins: [RevealMarkdown],
            });
        </script>
    </body>
</html>
```

If the bus is already present here, then it has nothing to do with mkslides. Please create an issue upstream instead of here.

---

**Describe the bug**

> A clear and concise description of what the bug is. If you have any error messages, also put the full error message here.

**To Reproduce**

> Steps to reproduce the behavior:
> 1. Go to '...'
> 2. Click on '....'
> 3. Scroll down to '....'
> 4. See error

**Expected behavior**

> A clear and concise description of what you expected to happen.

**Screenshots**

> If applicable, add screenshots to help explain your problem.

**Logs**

> If applicable, add logs to help explain your problem. Use the `--verbose` option to generate debug level output.

**Minimal reproducable example:**

> Add a minimal reproducable example with configuration file and markdown files. This is **essential** to be able to test and debug your problem.

**Version:**

> Use the `--version` option to generate version output.

**Additional context**

> Add any other context about the problem here.
