"""Figure <n>: <what the figure explains>.

Values: <source script and section, or file:line>: <the values used, copied from the source>.
"""

from figkit import row
from svglib import AMBER, BLUE, EMERALD, NEUTRAL, Diagram

d = Diagram(width=1100)
d.header("<title: what the figure explains>",
         "<Document>  ·  <section>  ·  <scope>",
         params="<one line with the key parameters>")

y = 116
d.panel(y, 170, 1, "<question?>", "<answer in one sentence>")
row(d, y + 74, [
    ("<box 1>", ["<line 1>", "<line 2>"], BLUE),
    ("<box 2>", ["<line 1>", "<line 2>"], AMBER),
    ("<box 3>", ["<line 1>", "<line 2>"], EMERALD),
], NEUTRAL[0])

y += 190
d.legend(30, y, [(BLUE, "<meaning>"), (AMBER, "<meaning>"), (EMERALD, "<meaning>")])
end = d.footnotes(30, y + 40, ["<what the figure simplifies>"])
d.save(height=end + 10)
