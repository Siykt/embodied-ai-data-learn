## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

This project is a documentation site for embodied AI data. Content should be written from the perspective of data collection, processing, alignment, annotation, quality control, evaluation, and dataset use, rather than as a generic algorithm learning site.

Writing requirements:

- Keep titles and navigation labels serious and professional. Do not use casual phrases such as "白话" or "说人话" in page titles, sidebar labels, card titles, or descriptions.
- Body content should still be easy to understand. Prefer clear Chinese explanations and everyday analogies when helpful, but keep the overall tone suitable for technical documentation.
- When a technical term is necessary, explain it in the relevant page and add or update a matching entry in the terminology documentation.
- For topics such as SLAM, robotics, sensors, calibration, or mapping, connect the discussion back to embodied AI data: inputs, outputs, alignment, data quality, evaluation, and downstream dataset usage.

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
