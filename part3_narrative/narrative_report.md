# Ethnic Wear Narrative Report

## May vs. April

### Context

This measures Ethnic Wear revenue from April to May: April revenue was `104520.77`, and May revenue was `185107.61`.

### Insight

**Fact:** Ethnic Wear revenue increased `77.1%` month on month from April to May, so the result is flagged.

### Implication

**Hypothesis:** The regional manager should review the May Ethnic Wear order mix and reseller-level performance, then check the related stock, price, and promotion records before deciding where to extend replenishment or promotional support.

## June vs. May

### Context

This measures Ethnic Wear revenue from May to June: May revenue was `185107.61`, and June revenue was `76371.53`.

### Insight

**Fact:** Ethnic Wear revenue decreased `58.74%` month on month from May to June, so the result is flagged in the opposite direction.

### Implication

**Hypothesis:** The regional manager should compare June stock availability, order-status mix, reseller-level performance, and price or promotion records with May before restoring inventory or changing regional support.

## Refinement Self-Score

- **Specificity:** Passes because both blocks name Ethnic Wear, identify the month comparisons, and use the supplied revenue and MoM values.
- **Audience fit:** Passes because the recommendations focus on regional allocation, reseller performance, inventory, pricing, and promotions rather than implementation details.
- **Completeness:** Passes because each block includes Context, Insight, and Implication, with the insight explicitly labeled as a Fact and the recommendation as a Hypothesis.
- **Actionability:** Passes because each recommendation names concrete records and comparisons to review before making an allocation or support decision.

## Chart-Choice Justification

### Which Month Had the Highest Total Revenue?

Use a vertical bar chart with month on the x-axis and total revenue on the y-axis. This is a bivariate comparison of one categorical variable (month) and one numeric variable (revenue), rather than a multivariate view, so a single-series bar chart communicates the ranking clearly within ten seconds. The y-axis should start at zero, the bars should show April at INR 419417.43, May at INR 444594.25, and June at INR 398055.24, and no legend is needed because there is only one series. Avoid 3D styling because it can distort the comparison.

### What Percentage Share Does Ethnic Wear Represent of April's Total Revenue?

Use a 100% stacked bar chart showing Ethnic Wear against the remainder of April revenue, with the Ethnic Wear segment labeled 24.92%. This is a univariate composition question about one total and its parts, not a multivariate comparison; the single normalized bar makes the part-to-whole message clear within ten seconds. A y-axis is not required for the composition, but if shown it should run from zero to 100%; use a legend because there are two segments, avoid 3D effects, and label the Ethnic Wear share directly. The underlying values are INR 104520.77 of INR 419417.43.

### How Do the Four Regions Compare on Total Revenue?

Use a sorted horizontal bar chart with region on the y-axis and total revenue on the x-axis: North at INR 337125.46, South at INR 316736.68, West at INR 333106.33, and East at INR 275098.45. This is a bivariate comparison of region and revenue, with no need for a multivariate chart because there is one measure and one series. A zero-based x-axis and direct data labels make the ranking clear within ten seconds; no legend is needed for a single series, and 3D should be avoided because it can obscure the magnitude differences.

## Top-Reseller Narrative

### Context

The Part 1 top-reseller query identifies five resellers whose total spend exceeded the threshold. The results are grouped by region and represented only by coded aliases: West includes `ALIAS-19` at INR 75295.09 and `ALIAS-22` at INR 73882.33; South includes `ALIAS-12` at INR 69936.46; and North includes `ALIAS-06` at INR 64238.97 and `ALIAS-05` at INR 61825.02.

### Insight

**Fact:** The five highest-spend reseller records are concentrated in West, South, and North, with the largest supplied total spend belonging to `ALIAS-19` in West at INR 75295.09.

### Implication

**Hypothesis:** The regional manager should review the order mix, service levels, and replenishment needs for `ALIAS-19`, `ALIAS-22`, `ALIAS-12`, `ALIAS-06`, and `ALIAS-05` by region, then assign the next account review and inventory-support actions without exposing raw reseller names.
