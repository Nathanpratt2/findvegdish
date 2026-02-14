# Feed Health Report
**Last Run:** 2026-02-14 14:20:21

### 📊 System Summary
| Metric | Value | Breakdown |
| :--- | :--- | :--- |
| **Total Database** | 1850 | 179 new today |
| **Blogs Monitored** | 108 | 30 HTML / 76 RSS |
| **Active Sources** | 93 | Sources with 5+ recipes |
| **WFPB Recipes** | 210 | 11% of total |
| **Easy Recipes** | 409 | 22% of total |
| **Budget Recipes** | 262 | 14% of total |
| **Gluten-Free** | 153 | 8% of total |
| **Avg Freshness** | 2025-08-03 | Latest post average |

---

### 📋 Detailed Blog Status
> **Tip:** Use the scroll bar in the box below to view all blogs. Click headers to sort.


<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("statusTable");
  switching = true;
  dir = "asc";
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      var xContent = x.innerText.toLowerCase();
      var yContent = y.innerText.toLowerCase();
      var xNum = parseFloat(xContent);
      var yNum = parseFloat(yContent);
      // Sort numerically only if both are numbers AND not dates (contain hyphen)
      if (!isNaN(xNum) && !isNaN(yNum) && /^\d/.test(xContent) && xContent.indexOf('-') === -1) {
          xContent = xNum; yContent = yNum;
      }
      if (dir == "asc") {
        if (xContent > yContent) { shouldSwitch = true; break; }
      } else if (dir == "desc") {
        if (xContent < yContent) { shouldSwitch = true; break; }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;
    } else {
      if (switchcount == 0 && dir == "asc") { dir = "desc"; switching = true; }
    }
  }
}
</script>
<style>
  #statusTable th { cursor: pointer; background-color: #f2f2f2; position: sticky; top: 0; z-index: 1; user-select: none; }
  #statusTable th:hover { background-color: #ddd; }
  #statusTable { border-collapse: collapse; width: 100%; font-family: sans-serif; }
  #statusTable th, #statusTable td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; font-size: 14px; }
  #statusTable tr:hover { background-color: #f9f9f9; }
</style>
<div style="height:600px; overflow-y:auto; border:1px solid #ddd; padding:0; border-radius:5px;">
<table id="statusTable">
<thead>
<tr>
 <th onclick="sortTable(0)">Blog Name &#8693;</th>
 <th onclick="sortTable(1)">New &#8693;</th>
 <th onclick="sortTable(2)">Total &#8693;</th>
 <th onclick="sortTable(3)">WFPB &#8693;</th>
 <th onclick="sortTable(4)">Easy &#8693;</th>
 <th onclick="sortTable(5)">Budg &#8693;</th>
 <th onclick="sortTable(6)">GF &#8693;</th>
 <th onclick="sortTable(7)">Latest &#8693;</th>
 <th onclick="sortTable(8)">Status &#8693;</th>
</tr>
</thead>
<tbody>
<tr><td>Cookie and Kate (Vegan Recipes)</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N/A</td><td>❌ No Recipes (0 Found)</td></tr>
<tr><td>No Meat Disco</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N/A</td><td>❌ No Recipes (0 Found)</td></tr>
<tr><td>Oh She Glows</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N/A</td><td>❌ No Recipes (0 Found)</td></tr>
<tr><td>Vegan Huggs</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N/A</td><td>❌ No Recipes (0 Found)</td></tr>
<tr><td>Baking Hermann</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2023-06-02</td><td>⚠️ Low Count</td></tr>
<tr><td>Chef AJ</td><td>0</td><td>3</td><td>3</td><td>0</td><td>1</td><td>0</td><td>2025-04-24</td><td>⚠️ Low Count</td></tr>
<tr><td>Dreena Burton</td><td>0</td><td>3</td><td>3</td><td>1</td><td>2</td><td>0</td><td>2026-01-20</td><td>⚠️ Low Count</td></tr>
<tr><td>Healthier Steps</td><td>0</td><td>2</td><td>1</td><td>0</td><td>0</td><td>0</td><td>2025-05-18</td><td>⚠️ Low Count</td></tr>
<tr><td>It's Liv B</td><td>0</td><td>4</td><td>0</td><td>2</td><td>1</td><td>0</td><td>2025-12-30</td><td>⚠️ Low Count</td></tr>
<tr><td>Minimalist Baker (Vegan Recipes)</td><td>0</td><td>4</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2026-02-10</td><td>⚠️ Low Count</td></tr>
<tr><td>One Arab Vegan</td><td>0</td><td>2</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2025-12-04</td><td>⚠️ Low Count</td></tr>
<tr><td>Snixy Kitchen (Vegan Recipes)</td><td>0</td><td>2</td><td>0</td><td>1</td><td>0</td><td>0</td><td>2025-11-21</td><td>⚠️ Low Count</td></tr>
<tr><td>Turnip Vegan</td><td>1</td><td>4</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2025-03-21</td><td>⚠️ Low Count</td></tr>
<tr><td>Vegan in the Freezer</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2026-02-11</td><td>⚠️ Low Count</td></tr>
<tr><td>Zacchary Bird</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2020-01-01</td><td>⚠️ Low Count</td></tr>
<tr><td>A Virtual Vegan</td><td>0</td><td>9</td><td>0</td><td>1</td><td>0</td><td>0</td><td>2026-02-06</td><td>✅ OK</td></tr>
<tr><td>Addicted to Dates</td><td>0</td><td>10</td><td>0</td><td>1</td><td>2</td><td>0</td><td>2026-01-30</td><td>✅ OK</td></tr>
<tr><td>Alison Roman (Vegan)</td><td>0</td><td>29</td><td>8</td><td>0</td><td>8</td><td>0</td><td>2025-08-11</td><td>✅ OK</td></tr>
<tr><td>Ann Arbor Vegan Kitchen</td><td>0</td><td>10</td><td>10</td><td>0</td><td>3</td><td>0</td><td>2026-02-04</td><td>✅ OK</td></tr>
<tr><td>Bianca Zapatka</td><td>0</td><td>10</td><td>2</td><td>5</td><td>2</td><td>1</td><td>2025-12-11</td><td>✅ OK</td></tr>
<tr><td>Big Box Vegan</td><td>2</td><td>8</td><td>0</td><td>2</td><td>0</td><td>0</td><td>2026-02-09</td><td>✅ OK</td></tr>
<tr><td>Cadry's Kitchen</td><td>5</td><td>5</td><td>0</td><td>3</td><td>0</td><td>0</td><td>2026-01-26</td><td>✅ OK</td></tr>
<tr><td>Chef Bai</td><td>1</td><td>63</td><td>3</td><td>11</td><td>1</td><td>1</td><td>2025-01-15</td><td>✅ OK (1)</td></tr>
<tr><td>Choosing Chia (Vegan Recipes)</td><td>0</td><td>5</td><td>0</td><td>5</td><td>0</td><td>0</td><td>2025-08-18</td><td>✅ OK</td></tr>
<tr><td>Connoisseurus Veg</td><td>0</td><td>11</td><td>0</td><td>1</td><td>1</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Cupful of Kale</td><td>9</td><td>6</td><td>1</td><td>0</td><td>0</td><td>0</td><td>2023-10-11</td><td>✅ OK (9)</td></tr>
<tr><td>Dr. Vegan</td><td>0</td><td>11</td><td>3</td><td>11</td><td>7</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Earth to Veg</td><td>2</td><td>8</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2026-02-06</td><td>✅ OK</td></tr>
<tr><td>Eat Figs, Not Pigs</td><td>0</td><td>14</td><td>0</td><td>5</td><td>1</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Elavegan</td><td>0</td><td>10</td><td>1</td><td>1</td><td>2</td><td>9</td><td>2026-02-06</td><td>✅ OK</td></tr>
<tr><td>Elsa's Wholesome Life</td><td>1</td><td>20</td><td>1</td><td>0</td><td>0</td><td>0</td><td>2022-02-14</td><td>✅ OK (1)</td></tr>
<tr><td>Flora & Vino</td><td>1</td><td>10</td><td>10</td><td>0</td><td>0</td><td>0</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>Forks Over Knives</td><td>1</td><td>10</td><td>10</td><td>2</td><td>2</td><td>1</td><td>2026-02-10</td><td>✅ OK</td></tr>
<tr><td>Fragrant Vanilla Cake</td><td>0</td><td>10</td><td>0</td><td>1</td><td>0</td><td>0</td><td>2026-02-09</td><td>✅ OK</td></tr>
<tr><td>From My Bowl</td><td>0</td><td>11</td><td>4</td><td>4</td><td>2</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Full of Plants</td><td>0</td><td>7</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Gaz Oakley</td><td>0</td><td>56</td><td>1</td><td>2</td><td>3</td><td>0</td><td>2020-01-01</td><td>✅ OK</td></tr>
<tr><td>Gretchen's Vegan Bakery</td><td>0</td><td>18</td><td>0</td><td>4</td><td>0</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>Healthy Little Vittles</td><td>1</td><td>20</td><td>0</td><td>5</td><td>1</td><td>20</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>HealthyGirl Kitchen</td><td>3</td><td>8</td><td>1</td><td>3</td><td>0</td><td>0</td><td>2026-02-06</td><td>✅ OK</td></tr>
<tr><td>Holistic Chef Academy</td><td>0</td><td>10</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2026-01-30</td><td>✅ OK</td></tr>
<tr><td>Hot For Food</td><td>1</td><td>150</td><td>10</td><td>23</td><td>9</td><td>0</td><td>2025-05-28</td><td>✅ OK (1)</td></tr>
<tr><td>It Doesn't Taste Like Chicken</td><td>0</td><td>32</td><td>1</td><td>14</td><td>9</td><td>0</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>Jessica in the Kitchen</td><td>0</td><td>12</td><td>1</td><td>2</td><td>1</td><td>2</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Lazy Cat Kitchen</td><td>0</td><td>10</td><td>0</td><td>0</td><td>2</td><td>0</td><td>2026-02-07</td><td>✅ OK</td></tr>
<tr><td>Love and Lemons (Vegan Recipes)</td><td>4</td><td>25</td><td>4</td><td>4</td><td>2</td><td>0</td><td>2026-02-05</td><td>✅ OK (4)</td></tr>
<tr><td>Make It Dairy Free</td><td>2</td><td>8</td><td>1</td><td>1</td><td>2</td><td>1</td><td>2026-02-01</td><td>✅ OK</td></tr>
<tr><td>Mary's Test Kitchen</td><td>4</td><td>6</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2026-02-03</td><td>✅ OK</td></tr>
<tr><td>Max La Manna</td><td>1</td><td>32</td><td>2</td><td>2</td><td>2</td><td>1</td><td>2020-01-01</td><td>✅ OK (1)</td></tr>
<tr><td>Messy Vegan Cook</td><td>0</td><td>13</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2026-01-02</td><td>✅ OK</td></tr>
<tr><td>Monkey & Me Kitchen Adventures</td><td>0</td><td>11</td><td>11</td><td>1</td><td>2</td><td>0</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>My Darling Vegan</td><td>1</td><td>12</td><td>1</td><td>2</td><td>1</td><td>0</td><td>2026-02-03</td><td>✅ OK</td></tr>
<tr><td>My Goodness Kitchen</td><td>0</td><td>5</td><td>2</td><td>1</td><td>0</td><td>0</td><td>2025-11-16</td><td>✅ OK</td></tr>
<tr><td>My Vegan Minimalist</td><td>0</td><td>7</td><td>1</td><td>5</td><td>0</td><td>0</td><td>2026-02-04</td><td>✅ OK</td></tr>
<tr><td>Nadia's Healthy Kitchen (Vegan Recipes)</td><td>1</td><td>22</td><td>6</td><td>2</td><td>2</td><td>1</td><td>2026-02-10</td><td>✅ OK (1)</td></tr>
<tr><td>Namely Marly</td><td>0</td><td>57</td><td>4</td><td>7</td><td>5</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>Nora Cooks</td><td>1</td><td>11</td><td>1</td><td>0</td><td>0</td><td>0</td><td>2026-02-09</td><td>✅ OK</td></tr>
<tr><td>NutritionFacts.org</td><td>1</td><td>12</td><td>12</td><td>0</td><td>3</td><td>0</td><td>2025-10-28</td><td>✅ OK</td></tr>
<tr><td>Pick Up Limes</td><td>1</td><td>14</td><td>0</td><td>0</td><td>2</td><td>0</td><td>2026-02-11</td><td>✅ OK (1)</td></tr>
<tr><td>Picky Eater (Vegan Options)</td><td>10</td><td>10</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Plant Baes</td><td>1</td><td>9</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2026-02-06</td><td>✅ OK</td></tr>
<tr><td>Plant Power Couple</td><td>0</td><td>12</td><td>0</td><td>12</td><td>1</td><td>0</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>Plant-Based on a Budget</td><td>2</td><td>36</td><td>2</td><td>7</td><td>36</td><td>1</td><td>2026-02-09</td><td>✅ OK (2)</td></tr>
<tr><td>PlantYou</td><td>0</td><td>12</td><td>12</td><td>1</td><td>2</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>Plantifully Based</td><td>1</td><td>11</td><td>1</td><td>3</td><td>0</td><td>0</td><td>2026-02-14</td><td>✅ OK</td></tr>
<tr><td>Rabbit and Wolves</td><td>2</td><td>8</td><td>0</td><td>1</td><td>1</td><td>0</td><td>2026-01-19</td><td>✅ OK</td></tr>
<tr><td>Rainbow Nourishments</td><td>0</td><td>10</td><td>0</td><td>2</td><td>1</td><td>0</td><td>2026-02-06</td><td>✅ OK</td></tr>
<tr><td>Rainbow Plant Life</td><td>10</td><td>6</td><td>2</td><td>0</td><td>2</td><td>0</td><td>2026-01-29</td><td>✅ OK</td></tr>
<tr><td>Rainbow Plant Life GF</td><td>1</td><td>19</td><td>5</td><td>1</td><td>4</td><td>17</td><td>2026-01-29</td><td>✅ OK (1)</td></tr>
<tr><td>Rhian's Recipes</td><td>3</td><td>21</td><td>0</td><td>0</td><td>0</td><td>21</td><td>2026-01-28</td><td>✅ OK</td></tr>
<tr><td>Running on Real Food</td><td>1</td><td>11</td><td>11</td><td>0</td><td>2</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>Sarah's Vegan Kitchen</td><td>3</td><td>12</td><td>0</td><td>0</td><td>3</td><td>0</td><td>2026-02-04</td><td>✅ OK</td></tr>
<tr><td>School Night Vegan</td><td>0</td><td>117</td><td>5</td><td>19</td><td>6</td><td>2</td><td>2024-12-05</td><td>✅ OK</td></tr>
<tr><td>Simple Vegan Blog</td><td>1</td><td>7</td><td>0</td><td>7</td><td>0</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>Strength and Sunshine</td><td>0</td><td>10</td><td>2</td><td>10</td><td>2</td><td>10</td><td>2026-01-22</td><td>✅ OK</td></tr>
<tr><td>Sweet Potato Soul</td><td>0</td><td>10</td><td>0</td><td>1</td><td>1</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>Sweet Simple Vegan</td><td>19</td><td>43</td><td>0</td><td>11</td><td>1</td><td>0</td><td>2026-02-10</td><td>✅ OK (19)</td></tr>
<tr><td>The Banana Diaries</td><td>0</td><td>11</td><td>0</td><td>4</td><td>2</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>The Burger Dude</td><td>2</td><td>14</td><td>0</td><td>1</td><td>2</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>The Cheap Lazy Vegan</td><td>0</td><td>8</td><td>0</td><td>8</td><td>8</td><td>0</td><td>2026-01-09</td><td>✅ OK</td></tr>
<tr><td>The Conscious Plant Kitchen</td><td>0</td><td>11</td><td>3</td><td>1</td><td>0</td><td>1</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>The Edgy Veg</td><td>1</td><td>9</td><td>0</td><td>1</td><td>0</td><td>0</td><td>2024-03-18</td><td>✅ OK (1)</td></tr>
<tr><td>The First Mess</td><td>0</td><td>12</td><td>1</td><td>2</td><td>2</td><td>1</td><td>2026-02-05</td><td>✅ OK</td></tr>
<tr><td>The Foodie Takes Flight</td><td>0</td><td>10</td><td>0</td><td>10</td><td>2</td><td>0</td><td>2026-02-05</td><td>✅ OK</td></tr>
<tr><td>The Full Helping</td><td>0</td><td>5</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2026-01-19</td><td>Skipped</td></tr>
<tr><td>The Full Helping (Vegan Recipes)</td><td>5</td><td>32</td><td>3</td><td>5</td><td>6</td><td>0</td><td>2026-01-19</td><td>✅ OK (5)</td></tr>
<tr><td>The Hidden Veggies</td><td>1</td><td>10</td><td>1</td><td>1</td><td>10</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>The Korean Vegan</td><td>3</td><td>7</td><td>0</td><td>5</td><td>0</td><td>0</td><td>2026-02-12</td><td>✅ OK</td></tr>
<tr><td>The Little Blog of Vegan</td><td>0</td><td>11</td><td>0</td><td>6</td><td>0</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>The Loopy Whisk (Vegan Recipes)</td><td>1</td><td>11</td><td>0</td><td>4</td><td>0</td><td>10</td><td>2024-06-07</td><td>✅ OK (1)</td></tr>
<tr><td>The Plant-Based RD</td><td>1</td><td>10</td><td>3</td><td>0</td><td>0</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>The Post-Punk Kitchen</td><td>0</td><td>10</td><td>1</td><td>1</td><td>2</td><td>0</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>The Stingy Vegan</td><td>0</td><td>11</td><td>0</td><td>11</td><td>11</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>The Veg Space</td><td>19</td><td>65</td><td>3</td><td>6</td><td>9</td><td>0</td><td>2022-10-20</td><td>✅ OK (19)</td></tr>
<tr><td>The Vegan 8</td><td>1</td><td>10</td><td>2</td><td>10</td><td>10</td><td>0</td><td>2026-02-13</td><td>✅ OK</td></tr>
<tr><td>Unconventional Baker</td><td>0</td><td>10</td><td>0</td><td>0</td><td>0</td><td>10</td><td>2025-11-01</td><td>✅ OK</td></tr>
<tr><td>VegNews</td><td>0</td><td>17</td><td>2</td><td>2</td><td>0</td><td>0</td><td>2026-02-10</td><td>✅ OK</td></tr>
<tr><td>Vegan Heaven</td><td>0</td><td>9</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2026-01-06</td><td>✅ OK</td></tr>
<tr><td>Vegan Punks</td><td>0</td><td>76</td><td>1</td><td>48</td><td>7</td><td>0</td><td>2025-11-26</td><td>✅ OK</td></tr>
<tr><td>Vegan Richa</td><td>9</td><td>10</td><td>0</td><td>2</td><td>4</td><td>0</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>Vegan Richa GF</td><td>0</td><td>25</td><td>0</td><td>7</td><td>7</td><td>25</td><td>2026-02-11</td><td>✅ OK</td></tr>
<tr><td>Vegan Yack Attack</td><td>19</td><td>192</td><td>15</td><td>30</td><td>23</td><td>4</td><td>2025-07-27</td><td>✅ OK (19)</td></tr>
<tr><td>Veggiekins</td><td>0</td><td>10</td><td>1</td><td>10</td><td>0</td><td>10</td><td>2026-02-10</td><td>✅ OK</td></tr>
<tr><td>Veggies Don't Bite</td><td>0</td><td>17</td><td>0</td><td>1</td><td>2</td><td>0</td><td>2026-02-13</td><td>Skipped</td></tr>
<tr><td>Watch Learn Eat</td><td>1</td><td>10</td><td>0</td><td>10</td><td>2</td><td>1</td><td>2026-02-07</td><td>✅ OK</td></tr>
<tr><td>What Jew You Want to Eat</td><td>1</td><td>29</td><td>3</td><td>1</td><td>1</td><td>0</td><td>2021-10-20</td><td>✅ OK (1)</td></tr>
<tr><td>ZardyPlants</td><td>0</td><td>10</td><td>10</td><td>7</td><td>3</td><td>0</td><td>2025-11-08</td><td>✅ OK</td></tr>
<tr><td>Zucker & Jagdwurst</td><td>17</td><td>18</td><td>0</td><td>0</td><td>0</td><td>0</td><td>2020-01-01</td><td>✅ OK (17)</td></tr>
</tbody></table></div>

---
*Report generated automatically by FindVegDish Fetcher.*