# London schools within 10 miles with A-level APS per entry > 37

Source metric: DfE 2024 final institution-level `points_per_entry` for cohort `A level`, disadvantaged status `All students`. Distance filter: <=10 miles from central London using full postcode coordinates.

<style>
  .secondary-school-tool {
    margin: 1.25rem 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  .secondary-filter-bar {
    position: sticky;
    top: 0;
    z-index: 2;
    display: grid;
    grid-template-columns: repeat(4, minmax(160px, 1fr));
    gap: 0.75rem;
    padding: 1rem;
    border: 1px solid #d8dee8;
    border-radius: 16px;
    background: rgba(248, 250, 252, 0.94);
    box-shadow: 0 16px 36px rgba(15, 23, 42, 0.12);
    backdrop-filter: blur(10px);
  }
  .secondary-filter-bar label {
    display: grid;
    gap: 0.25rem;
    color: #475569;
    font-size: 0.78rem;
    font-weight: 700;
  }
  .secondary-filter-bar input,
  .secondary-filter-bar select {
    min-height: 2.25rem;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 0.45rem 0.6rem;
    background: white;
    color: #0f172a;
    font: inherit;
  }
  .secondary-filter-summary {
    grid-column: 1 / -1;
    color: #334155;
    font-size: 0.9rem;
    font-weight: 700;
  }
  .secondary-table-wrap {
    margin-top: 1rem;
    overflow: auto;
    border: 1px solid #d8dee8;
    border-radius: 16px;
    background: white;
  }
  .secondary-schools-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.88rem;
  }
  .secondary-schools-table th {
    position: sticky;
    top: 0;
    z-index: 1;
    background: #0f172a;
    color: white;
    text-align: left;
    vertical-align: bottom;
  }
  .secondary-schools-table th,
  .secondary-schools-table td {
    padding: 0.65rem 0.75rem;
    border-bottom: 1px solid #e2e8f0;
  }
  .secondary-schools-table tbody tr:nth-child(even) {
    background: #f8fafc;
  }
  .secondary-schools-table tbody tr:hover {
    background: #eef6ff;
  }
  .secondary-schools-table .numeric {
    text-align: right;
    font-variant-numeric: tabular-nums;
  }
  .sort-button {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    width: 100%;
    border: 0;
    padding: 0;
    background: transparent;
    color: inherit;
    cursor: pointer;
    font: inherit;
    font-weight: 800;
    text-align: left;
  }
  .secondary-notes {
    margin-top: 1rem;
    color: #475569;
    font-size: 0.9rem;
    line-height: 1.55;
  }
  @media (max-width: 900px) {
    .secondary-filter-bar {
      grid-template-columns: 1fr 1fr;
    }
  }
  @media (max-width: 620px) {
    .secondary-filter-bar {
      grid-template-columns: 1fr;
      position: static;
    }
  }
</style>

<div class="secondary-school-tool">
  <div class="secondary-filter-bar" aria-label="Secondary school filters">
    <label>Search
      <input id="secondarySearch" type="search" placeholder="School, borough, type, phase...">
    </label>
    <label>State/private
      <select id="secondaryStateFilter">
        <option value="">All</option>
<option value="Private">Private</option>
<option value="State">State</option>
      </select>
    </label>
    <label>Borough / area
      <select id="secondaryBoroughFilter">
        <option value="">All</option>
<option value="Barnet">Barnet</option>
<option value="Brent">Brent</option>
<option value="Bromley">Bromley</option>
<option value="Camden">Camden</option>
<option value="City of London">City of London</option>
<option value="Croydon">Croydon</option>
<option value="Ealing">Ealing</option>
<option value="Enfield">Enfield</option>
<option value="Greenwich">Greenwich</option>
<option value="Hackney">Hackney</option>
<option value="Hammersmith and Fulham">Hammersmith and Fulham</option>
<option value="Haringey">Haringey</option>
<option value="Hounslow">Hounslow</option>
<option value="Islington">Islington</option>
<option value="Kensington and Chelsea">Kensington and Chelsea</option>
<option value="Kingston upon Thames">Kingston upon Thames</option>
<option value="Lambeth">Lambeth</option>
<option value="Lewisham">Lewisham</option>
<option value="Merton">Merton</option>
<option value="Newham">Newham</option>
<option value="Richmond upon Thames">Richmond upon Thames</option>
<option value="Southwark">Southwark</option>
<option value="Sutton">Sutton</option>
<option value="Waltham Forest">Waltham Forest</option>
<option value="Wandsworth">Wandsworth</option>
<option value="Westminster">Westminster</option>
      </select>
    </label>
    <label>Phase
      <select id="secondaryPhaseFilter">
        <option value="">All</option>
<option value="11 to 17">11 to 17</option>
<option value="all-through">all-through</option>
<option value="partial all-through">partial all-through</option>
<option value="secondary-only">secondary-only</option>
<option value="sixth-form-only">sixth-form-only</option>
      </select>
    </label>
    <label>School type
      <select id="secondaryTypeFilter">
        <option value="">All</option>
<option value="Academy">Academy</option>
<option value="Community school">Community school</option>
<option value="Free school">Free school</option>
<option value="Free school 16-19">Free school 16-19</option>
<option value="Independent school">Independent school</option>
<option value="Sixth form college">Sixth form college</option>
<option value="Voluntary aided">Voluntary aided</option>
      </select>
    </label>
    <label>Selectivity
      <select id="secondarySelectivityFilter">
        <option value="">All</option>
<option value="academically selective/fee-paying">academically selective/fee-paying</option>
<option value="comprehensive/non-selective">comprehensive/non-selective</option>
<option value="comprehensive; selective sixth-form entry">comprehensive; selective sixth-form entry</option>
<option value="non-selective in selective area">non-selective in selective area</option>
<option value="not listed as academically selective">not listed as academically selective</option>
<option value="selective grammar">selective grammar</option>
<option value="selective sixth form">selective sixth form</option>
<option value="sixth-form admissions criteria">sixth-form admissions criteria</option>
<option value="specialist maths selective">specialist maths selective</option>
      </select>
    </label>
    <label>Minimum APS
      <input id="secondaryMinAps" type="number" min="0" step="0.1" placeholder="e.g. 45">
    </label>
    <label>Rows
      <select id="secondaryRowLimit">
        <option value="">All rows</option>
        <option value="25">Top 25</option>
        <option value="50">Top 50</option>
        <option value="100">Top 100</option>
      </select>
    </label>
    <div id="secondaryFilterSummary" class="secondary-filter-summary"></div>
  </div>
  <div class="secondary-table-wrap">
    <table id="secondarySchoolsTable" class="secondary-schools-table">
      <thead><tr>
<th><button class="sort-button" type="button" data-column="School" data-sort-type="text" aria-label="Sort by School">School <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="APS per A level entry" data-sort-type="number" aria-label="Sort by APS per A level entry">APS per A level entry <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Oxbridge applications (2022-2024)" data-sort-type="number" aria-label="Sort by Oxbridge applications (2022-2024)">Oxbridge applications (2022-2024) <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Oxbridge offers (2022-2024)" data-sort-type="number" aria-label="Sort by Oxbridge offers (2022-2024)">Oxbridge offers (2022-2024) <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Oxbridge offer rate" data-sort-type="number" aria-label="Sort by Oxbridge offer rate">Oxbridge offer rate <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Area / borough / town" data-sort-type="text" aria-label="Sort by Area / borough / town">Area / borough / town <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Postcode district" data-sort-type="text" aria-label="Sort by Postcode district">Postcode district <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="School type" data-sort-type="text" aria-label="Sort by School type">School type <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="State/private" data-sort-type="text" aria-label="Sort by State/private">State/private <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Approx annual fees" data-sort-type="text" aria-label="Sort by Approx annual fees">Approx annual fees <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Selectivity" data-sort-type="text" aria-label="Sort by Selectivity">Selectivity <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Further exam/selection after joining?" data-sort-type="text" aria-label="Sort by Further exam/selection after joining?">Further exam/selection after joining? <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="GCSE cut-off for sixth form?" data-sort-type="text" aria-label="Sort by GCSE cut-off for sixth form?">GCSE cut-off for sixth form? <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Phase" data-sort-type="text" aria-label="Sort by Phase">Phase <span aria-hidden="true">↕</span></button></th>
<th><button class="sort-button" type="button" data-column="Google Maps" data-sort-type="text" aria-label="Sort by Google Maps">Google Maps <span aria-hidden="true">↕</span></button></th>
</tr></thead>
<tbody>
<tr data-search="king&#x27;s college london maths school 56.11 195 91 47% lambeth se11 free school 16-19 state n/a specialist maths selective n/a after joining; entry is at 16+ via specialist maths selection yes - 16+ entry uses high gcse/predicted-grade thresholds sixth-form-only [map](https://www.google.com/maps/search/?api=1&amp;query=king%27s+college+london+maths+school+se11+6nj)" data-state="State" data-borough="Lambeth" data-phase="sixth-form-only" data-school-type="Free school 16-19" data-selectivity="specialist maths selective" data-aps="56.11">
<td data-column="School" data-sort-value="king&#x27;s college london maths school">King&#x27;s College London Maths School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="56.11">56.11</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="195.0">195</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="91.0">91</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="47.0">47%</td>
<td data-column="Area / borough / town" data-sort-value="lambeth">Lambeth</td>
<td data-column="Postcode district" data-sort-value="se11">SE11</td>
<td data-column="School type" data-sort-value="free school 16-19">Free school 16-19</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="specialist maths selective">specialist maths selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="n/a after joining; entry is at 16+ via specialist maths selection">N/A after joining; entry is at 16+ via specialist maths selection</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - 16+ entry uses high gcse/predicted-grade thresholds">Yes - 16+ entry uses high GCSE/predicted-grade thresholds</td>
<td data-column="Phase" data-sort-value="sixth-form-only">sixth-form-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=king%27s+college+london+maths+school+se11+6nj)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=King%27s+College+London+Maths+School+SE11+6NJ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st paul&#x27;s girls&#x27; school 54.75 264 140 53% hammersmith and fulham w6 independent school private ~£34k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=st+paul%27s+girls%27+school+w6+7bs)" data-state="Private" data-borough="Hammersmith and Fulham" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="54.75">
<td data-column="School" data-sort-value="st paul&#x27;s girls&#x27; school">St Paul&#x27;s Girls&#x27; School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="54.75">54.75</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="264.0">264</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="140.0">140</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="53.0">53%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="w6">W6</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£34k">~£34k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+paul%27s+girls%27+school+w6+7bs)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Paul%27s+Girls%27+School+W6+7BS" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st paul&#x27;s school 54.33 433 141 33% richmond upon thames sw13 independent school private ~£34k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=st+paul%27s+school+sw13+9jt)" data-state="Private" data-borough="Richmond upon Thames" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="54.33">
<td data-column="School" data-sort-value="st paul&#x27;s school">St Paul&#x27;s School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="54.33">54.33</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="433.0">433</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="141.0">141</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="33.0">33%</td>
<td data-column="Area / borough / town" data-sort-value="richmond upon thames">Richmond upon Thames</td>
<td data-column="Postcode district" data-sort-value="sw13">SW13</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£34k">~£34k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+paul%27s+school+sw13+9jt)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Paul%27s+School+SW13+9JT" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="westminster school 53.91 537 246 46% westminster sw1p independent school private ~£43k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=westminster+school+sw1p+3pf)" data-state="Private" data-borough="Westminster" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="53.91">
<td data-column="School" data-sort-value="westminster school">Westminster School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="53.91">53.91</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="537.0">537</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="246.0">246</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="46.0">46%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="sw1p">SW1P</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£43k">~£43k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=westminster+school+sw1p+3pf)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Westminster+School+SW1P+3PF" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="king&#x27;s college school 53.09 417 124 30% merton sw19 independent school private ~£31k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=king%27s+college+school+sw19+4tt)" data-state="Private" data-borough="Merton" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="53.09">
<td data-column="School" data-sort-value="king&#x27;s college school">King&#x27;s College School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="53.09">53.09</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="417.0">417</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="124.0">124</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="30.0">30%</td>
<td data-column="Area / borough / town" data-sort-value="merton">Merton</td>
<td data-column="Postcode district" data-sort-value="sw19">SW19</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£31k">~£31k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=king%27s+college+school+sw19+4tt)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=King%27s+College+School+SW19+4TT" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="wimbledon high school gdst 52.24 117 ≥21 ≥18% merton sw19 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=wimbledon+high+school+gdst+sw19+4ab)" data-state="Private" data-borough="Merton" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="52.24">
<td data-column="School" data-sort-value="wimbledon high school gdst">Wimbledon High School GDST</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="52.24">52.24</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="117.0">117</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="21.0">≥21</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="18.0">≥18%</td>
<td data-column="Area / borough / town" data-sort-value="merton">Merton</td>
<td data-column="Postcode district" data-sort-value="sw19">SW19</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=wimbledon+high+school+gdst+sw19+4ab)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Wimbledon+High+School+GDST+SW19+4AB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="city of london school for girls 52.21 180 49 27% city of london ec2y independent school private ~£31k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+school+for+girls+ec2y+8bb)" data-state="Private" data-borough="City of London" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="52.21">
<td data-column="School" data-sort-value="city of london school for girls">City of London School for Girls</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="52.21">52.21</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="180.0">180</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="49.0">49</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="27.0">27%</td>
<td data-column="Area / borough / town" data-sort-value="city of london">City of London</td>
<td data-column="Postcode district" data-sort-value="ec2y">EC2Y</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£31k">~£31k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+school+for+girls+ec2y+8bb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=City+of+London+School+for+Girls+EC2Y+8BB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the godolphin and latymer school 51.90 145 29 20% hammersmith and fulham w6 independent school private ~£32k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=the+godolphin+and+latymer+school+w6+0pg)" data-state="Private" data-borough="Hammersmith and Fulham" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="51.9">
<td data-column="School" data-sort-value="the godolphin and latymer school">The Godolphin and Latymer School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="51.9">51.90</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="145.0">145</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="29.0">29</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="20.0">20%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="w6">W6</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£32k">~£32k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+godolphin+and+latymer+school+w6+0pg)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Godolphin+and+Latymer+School+W6+0PG" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the henrietta barnett school 51.67 228 94 41% barnet nw11 academy state n/a selective grammar no new entrance exam for existing pupils yes - sixth-form subject/gcse thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+henrietta+barnett+school+nw11+7bn)" data-state="State" data-borough="Barnet" data-phase="secondary-only" data-school-type="Academy" data-selectivity="selective grammar" data-aps="51.67">
<td data-column="School" data-sort-value="the henrietta barnett school">The Henrietta Barnett School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="51.67">51.67</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="228.0">228</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="94.0">94</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="41.0">41%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="nw11">NW11</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective grammar">selective grammar</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no new entrance exam for existing pupils">No new entrance exam for existing pupils</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds apply">Yes - sixth-form subject/GCSE thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+henrietta+barnett+school+nw11+7bn)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Henrietta+Barnett+School+NW11+7BN" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="city of london school 51.40 263 84 32% city of london ec4v independent school private ~£32k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+school+ec4v+3al)" data-state="Private" data-borough="City of London" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="51.4">
<td data-column="School" data-sort-value="city of london school">City of London School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="51.4">51.40</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="263.0">263</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="84.0">84</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="32.0">32%</td>
<td data-column="Area / borough / town" data-sort-value="city of london">City of London</td>
<td data-column="Postcode district" data-sort-value="ec4v">EC4V</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£32k">~£32k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+school+ec4v+3al)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=City+of+London+School+EC4V+3AL" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="alleyn&#x27;s school 51.33 182 59 32% southwark se22 independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=alleyn%27s+school+se22+8su)" data-state="Private" data-borough="Southwark" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="51.33">
<td data-column="School" data-sort-value="alleyn&#x27;s school">Alleyn&#x27;s School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="51.33">51.33</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="182.0">182</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="59.0">59</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="32.0">32%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se22">SE22</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=alleyn%27s+school+se22+8su)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Alleyn%27s+School+SE22+8SU" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="highgate school 51.31 264 87 33% haringey n6 independent school private ~£30k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=highgate+school+n6+4ay)" data-state="Private" data-borough="Haringey" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="51.31">
<td data-column="School" data-sort-value="highgate school">Highgate School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="51.31">51.31</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="264.0">264</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="87.0">87</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="33.0">33%</td>
<td data-column="Area / borough / town" data-sort-value="haringey">Haringey</td>
<td data-column="Postcode district" data-sort-value="n6">N6</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£30k">~£30k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=highgate+school+n6+4ay)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Highgate+School+N6+4AY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="latymer upper school and latymer prep 51.30 261 75 29% hammersmith and fulham w6 independent school private ~£30k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=latymer+upper+school+and+latymer+prep+w6+9lr)" data-state="Private" data-borough="Hammersmith and Fulham" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="51.3">
<td data-column="School" data-sort-value="latymer upper school and latymer prep">Latymer Upper School and Latymer Prep</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="51.3">51.30</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="261.0">261</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="75.0">75</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="29.0">29%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="w6">W6</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£30k">~£30k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=latymer+upper+school+and+latymer+prep+w6+9lr)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Latymer+Upper+School+and+Latymer+Prep+W6+9LR" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="putney high school 50.55 108 34 31% wandsworth sw15 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=putney+high+school+sw15+6bh)" data-state="Private" data-borough="Wandsworth" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="50.55">
<td data-column="School" data-sort-value="putney high school">Putney High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="50.55">50.55</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="108.0">108</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="34.0">34</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="31.0">31%</td>
<td data-column="Area / borough / town" data-sort-value="wandsworth">Wandsworth</td>
<td data-column="Postcode district" data-sort-value="sw15">SW15</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=putney+high+school+sw15+6bh)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Putney+High+School+SW15+6BH" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="south hampstead high school 50.45 122 43 35% camden nw3 independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=south+hampstead+high+school+nw3+5ss)" data-state="Private" data-borough="Camden" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="50.45">
<td data-column="School" data-sort-value="south hampstead high school">South Hampstead High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="50.45">50.45</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="122.0">122</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="43.0">43</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="35.0">35%</td>
<td data-column="Area / borough / town" data-sort-value="camden">Camden</td>
<td data-column="Postcode district" data-sort-value="nw3">NW3</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=south+hampstead+high+school+nw3+5ss)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=South+Hampstead+High+School+NW3+5SS" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="kingston grammar school 49.97 95 ≥19 ≥20% kingston upon thames kt2 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=kingston+grammar+school+kt2+6py)" data-state="Private" data-borough="Kingston upon Thames" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="49.97">
<td data-column="School" data-sort-value="kingston grammar school">Kingston Grammar School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.97">49.97</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="95.0">95</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="19.0">≥19</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="20.0">≥20%</td>
<td data-column="Area / borough / town" data-sort-value="kingston upon thames">Kingston upon Thames</td>
<td data-column="Postcode district" data-sort-value="kt2">KT2</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=kingston+grammar+school+kt2+6py)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Kingston+Grammar+School+KT2+6PY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the tiffin girls&#x27; school 49.94 221 65 29% kingston upon thames kt2 academy state n/a selective grammar no new entrance exam for existing pupils yes - sixth-form subject/gcse thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+tiffin+girls%27+school+kt2+5pl)" data-state="State" data-borough="Kingston upon Thames" data-phase="secondary-only" data-school-type="Academy" data-selectivity="selective grammar" data-aps="49.94">
<td data-column="School" data-sort-value="the tiffin girls&#x27; school">The Tiffin Girls&#x27; School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.94">49.94</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="221.0">221</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="65.0">65</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="29.0">29%</td>
<td data-column="Area / borough / town" data-sort-value="kingston upon thames">Kingston upon Thames</td>
<td data-column="Postcode district" data-sort-value="kt2">KT2</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective grammar">selective grammar</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no new entrance exam for existing pupils">No new entrance exam for existing pupils</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds apply">Yes - sixth-form subject/GCSE thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+tiffin+girls%27+school+kt2+5pl)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Tiffin+Girls%27+School+KT2+5PL" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="james allen&#x27;s girls&#x27; school 49.75 130 52 40% southwark se22 independent school private ~£30k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=james+allen%27s+girls%27+school+se22+8te)" data-state="Private" data-borough="Southwark" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="49.75">
<td data-column="School" data-sort-value="james allen&#x27;s girls&#x27; school">James Allen&#x27;s Girls&#x27; School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.75">49.75</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="130.0">130</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="52.0">52</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="40.0">40%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se22">SE22</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£30k">~£30k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=james+allen%27s+girls%27+school+se22+8te)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=James+Allen%27s+Girls%27+School+SE22+8TE" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="brampton manor academy 49.67 872 193 22% newham e6 academy state n/a comprehensive; selective sixth-form entry no separate internal exam noted; sixth form is academically selective by grades yes - sixth-form gcse/predicted-grade thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=brampton+manor+academy+e6+3sq)" data-state="State" data-borough="Newham" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive; selective sixth-form entry" data-aps="49.67">
<td data-column="School" data-sort-value="brampton manor academy">Brampton Manor Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.67">49.67</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="872.0">872</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="193.0">193</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="22.0">22%</td>
<td data-column="Area / borough / town" data-sort-value="newham">Newham</td>
<td data-column="Postcode district" data-sort-value="e6">E6</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive; selective sixth-form entry">comprehensive; selective sixth-form entry</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no separate internal exam noted; sixth form is academically selective by grades">No separate internal exam noted; sixth form is academically selective by grades</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form gcse/predicted-grade thresholds apply">Yes - sixth-form GCSE/predicted-grade thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=brampton+manor+academy+e6+3sq)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Brampton+Manor+Academy+E6+3SQ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="london academy of excellence 49.49 270 86 32% newham e15 free school 16-19 state n/a selective sixth form n/a after joining; entry is at 16+ via selective sixth-form admissions yes - 16+ entry uses gcse/predicted-grade thresholds sixth-form-only [map](https://www.google.com/maps/search/?api=1&amp;query=london+academy+of+excellence+e15+1aj)" data-state="State" data-borough="Newham" data-phase="sixth-form-only" data-school-type="Free school 16-19" data-selectivity="selective sixth form" data-aps="49.49">
<td data-column="School" data-sort-value="london academy of excellence">London Academy of Excellence</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.49">49.49</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="270.0">270</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="86.0">86</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="32.0">32%</td>
<td data-column="Area / borough / town" data-sort-value="newham">Newham</td>
<td data-column="Postcode district" data-sort-value="e15">E15</td>
<td data-column="School type" data-sort-value="free school 16-19">Free school 16-19</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective sixth form">selective sixth form</td>
<td data-column="Further exam/selection after joining?" data-sort-value="n/a after joining; entry is at 16+ via selective sixth-form admissions">N/A after joining; entry is at 16+ via selective sixth-form admissions</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - 16+ entry uses gcse/predicted-grade thresholds">Yes - 16+ entry uses GCSE/predicted-grade thresholds</td>
<td data-column="Phase" data-sort-value="sixth-form-only">sixth-form-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=london+academy+of+excellence+e15+1aj)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=London+Academy+of+Excellence+E15+1AJ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="tiffin school 49.21 403 113 28% kingston upon thames kt2 academy state n/a selective grammar no new entrance exam for existing pupils yes - sixth-form subject/gcse thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=tiffin+school+kt2+6rl)" data-state="State" data-borough="Kingston upon Thames" data-phase="secondary-only" data-school-type="Academy" data-selectivity="selective grammar" data-aps="49.21">
<td data-column="School" data-sort-value="tiffin school">Tiffin School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.21">49.21</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="403.0">403</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="113.0">113</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="28.0">28%</td>
<td data-column="Area / borough / town" data-sort-value="kingston upon thames">Kingston upon Thames</td>
<td data-column="Postcode district" data-sort-value="kt2">KT2</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective grammar">selective grammar</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no new entrance exam for existing pupils">No new entrance exam for existing pupils</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds apply">Yes - sixth-form subject/GCSE thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=tiffin+school+kt2+6rl)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Tiffin+School+KT2+6RL" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="michaela community school 49.17 31 ≥10 ≥32% brent ha9 free school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=michaela+community+school+ha9+0uu)" data-state="State" data-borough="Brent" data-phase="secondary-only" data-school-type="Free school" data-selectivity="comprehensive/non-selective" data-aps="49.17">
<td data-column="School" data-sort-value="michaela community school">Michaela Community School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.17">49.17</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="31.0">31</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="10.0">≥10</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="32.0">≥32%</td>
<td data-column="Area / borough / town" data-sort-value="brent">Brent</td>
<td data-column="Postcode district" data-sort-value="ha9">HA9</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=michaela+community+school+ha9+0uu)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Michaela+Community+School+HA9+0UU" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="notting hill &amp; ealing high school gdst 49.12 69 ≥17 ≥25% ealing w13 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=notting+hill+%26+ealing+high+school+gdst+w13+8ax)" data-state="Private" data-borough="Ealing" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="49.12">
<td data-column="School" data-sort-value="notting hill &amp; ealing high school gdst">Notting Hill &amp; Ealing High School GDST</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="49.12">49.12</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="69.0">69</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="17.0">≥17</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="25.0">≥25%</td>
<td data-column="Area / borough / town" data-sort-value="ealing">Ealing</td>
<td data-column="Postcode district" data-sort-value="w13">W13</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=notting+hill+%26+ealing+high+school+gdst+w13+8ax)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Notting+Hill+%26+Ealing+High+School+GDST+W13+8AX" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="university college school 48.91 225 51 23% camden nw3 independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=university+college+school+nw3+6xh)" data-state="Private" data-borough="Camden" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="48.91">
<td data-column="School" data-sort-value="university college school">University College School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="48.91">48.91</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="225.0">225</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="51.0">51</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="23.0">23%</td>
<td data-column="Area / borough / town" data-sort-value="camden">Camden</td>
<td data-column="Postcode district" data-sort-value="nw3">NW3</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=university+college+school+nw3+6xh)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=University+College+School+NW3+6XH" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="francis holland school 48.78 37 ≥7 ≥19% westminster sw1w independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=francis+holland+school+sw1w+8jf)" data-state="Private" data-borough="Westminster" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="48.78">
<td data-column="School" data-sort-value="francis holland school">Francis Holland School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="48.78">48.78</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="37.0">37</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="7.0">≥7</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="19.0">≥19%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="sw1w">SW1W</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=francis+holland+school+sw1w+8jf)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Francis+Holland+School+SW1W+8JF" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="trinity school 48.73 148 40 27% croydon cr9 independent school private ~£25k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=trinity+school+cr9+7at)" data-state="Private" data-borough="Croydon" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="48.73">
<td data-column="School" data-sort-value="trinity school">Trinity School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="48.73">48.73</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="148.0">148</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="40.0">40</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="27.0">27%</td>
<td data-column="Area / borough / town" data-sort-value="croydon">Croydon</td>
<td data-column="Postcode district" data-sort-value="cr9">CR9</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£25k">~£25k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=trinity+school+cr9+7at)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Trinity+School+CR9+7AT" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="newham collegiate sixth form centre, city of london academy 48.68 365 78 21% newham e6 free school 16-19 state n/a selective sixth form n/a after joining; entry is at 16+ via selective sixth-form admissions yes - 16+ entry uses gcse/predicted-grade thresholds sixth-form-only [map](https://www.google.com/maps/search/?api=1&amp;query=newham+collegiate+sixth+form+centre%2c+city+of+london+academy+e6+2bb)" data-state="State" data-borough="Newham" data-phase="sixth-form-only" data-school-type="Free school 16-19" data-selectivity="selective sixth form" data-aps="48.68">
<td data-column="School" data-sort-value="newham collegiate sixth form centre, city of london academy">Newham Collegiate Sixth Form Centre, City of London Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="48.68">48.68</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="365.0">365</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="78.0">78</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="21.0">21%</td>
<td data-column="Area / borough / town" data-sort-value="newham">Newham</td>
<td data-column="Postcode district" data-sort-value="e6">E6</td>
<td data-column="School type" data-sort-value="free school 16-19">Free school 16-19</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective sixth form">selective sixth form</td>
<td data-column="Further exam/selection after joining?" data-sort-value="n/a after joining; entry is at 16+ via selective sixth-form admissions">N/A after joining; entry is at 16+ via selective sixth-form admissions</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - 16+ entry uses gcse/predicted-grade thresholds">Yes - 16+ entry uses GCSE/predicted-grade thresholds</td>
<td data-column="Phase" data-sort-value="sixth-form-only">sixth-form-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=newham+collegiate+sixth+form+centre%2c+city+of+london+academy+e6+2bb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Newham+Collegiate+Sixth+Form+Centre%2C+City+of+London+Academy+E6+2BB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="queen&#x27;s college, london 48.40 26 ≥5 ≥19% westminster w1g independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=queen%27s+college%2c+london+w1g+8bt)" data-state="Private" data-borough="Westminster" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="48.4">
<td data-column="School" data-sort-value="queen&#x27;s college, london">Queen&#x27;s College, London</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="48.4">48.40</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="26.0">26</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="19.0">≥19%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="w1g">W1G</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=queen%27s+college%2c+london+w1g+8bt)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Queen%27s+College%2C+London+W1G+8BT" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="channing school 48.27 44 ≥8 ≥18% haringey n6 independent school private ~£28k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=channing+school+n6+5hf)" data-state="Private" data-borough="Haringey" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="48.27">
<td data-column="School" data-sort-value="channing school">Channing School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="48.27">48.27</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="44.0">44</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="18.0">≥18%</td>
<td data-column="Area / borough / town" data-sort-value="haringey">Haringey</td>
<td data-column="Postcode district" data-sort-value="n6">N6</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£28k">~£28k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=channing+school+n6+5hf)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Channing+School+N6+5HF" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="eltham college 48.21 100 25 25% bromley se9 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=eltham+college+se9+4qf)" data-state="Private" data-borough="Bromley" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="48.21">
<td data-column="School" data-sort-value="eltham college">Eltham College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="48.21">48.21</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="100.0">100</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="25.0">25</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="25.0">25%</td>
<td data-column="Area / borough / town" data-sort-value="bromley">Bromley</td>
<td data-column="Postcode district" data-sort-value="se9">SE9</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=eltham+college+se9+4qf)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Eltham+College+SE9+4QF" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="emanuel school 47.94 55 ≥21 ≥38% wandsworth sw11 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=emanuel+school+sw11+1hs)" data-state="Private" data-borough="Wandsworth" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="47.94">
<td data-column="School" data-sort-value="emanuel school">Emanuel School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="47.94">47.94</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="55.0">55</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="21.0">≥21</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="38.0">≥38%</td>
<td data-column="Area / borough / town" data-sort-value="wandsworth">Wandsworth</td>
<td data-column="Postcode district" data-sort-value="sw11">SW11</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=emanuel+school+sw11+1hs)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Emanuel+School+SW11+1HS" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="dulwich college 47.92 274 60 22% southwark se21 independent school private ~£31k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=dulwich+college+se21+7ld)" data-state="Private" data-borough="Southwark" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="47.92">
<td data-column="School" data-sort-value="dulwich college">Dulwich College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="47.92">47.92</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="274.0">274</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="60.0">60</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="22.0">22%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se21">SE21</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£31k">~£31k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=dulwich+college+se21+7ld)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Dulwich+College+SE21+7LD" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the latymer school 47.28 241 58 24% enfield n9 voluntary aided state n/a selective grammar no new entrance exam for existing pupils yes - sixth-form subject/gcse thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+latymer+school+n9+9tn)" data-state="State" data-borough="Enfield" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="selective grammar" data-aps="47.28">
<td data-column="School" data-sort-value="the latymer school">The Latymer School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="47.28">47.28</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="241.0">241</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="58.0">58</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="24.0">24%</td>
<td data-column="Area / borough / town" data-sort-value="enfield">Enfield</td>
<td data-column="Postcode district" data-sort-value="n9">N9</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective grammar">selective grammar</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no new entrance exam for existing pupils">No new entrance exam for existing pupils</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds apply">Yes - sixth-form subject/GCSE thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+latymer+school+n9+9tn)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Latymer+School+N9+9TN" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st augustine&#x27;s priory 46.97 ≥9 ≥0 ≥0% ealing w5 independent school private ~£22k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=st+augustine%27s+priory+w5+2jl)" data-state="Private" data-borough="Ealing" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="46.97">
<td data-column="School" data-sort-value="st augustine&#x27;s priory">St Augustine&#x27;s Priory</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.97">46.97</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="ealing">Ealing</td>
<td data-column="Postcode district" data-sort-value="w5">W5</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£22k">~£22k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+augustine%27s+priory+w5+2jl)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Augustine%27s+Priory+W5+2JL" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="wallington county grammar school 46.95 137 28 20% sutton sm6 academy state n/a selective grammar no new entrance exam for existing pupils yes - sixth-form subject/gcse thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=wallington+county+grammar+school+sm6+7ph)" data-state="State" data-borough="Sutton" data-phase="secondary-only" data-school-type="Academy" data-selectivity="selective grammar" data-aps="46.95">
<td data-column="School" data-sort-value="wallington county grammar school">Wallington County Grammar School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.95">46.95</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="137.0">137</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="28.0">28</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="20.0">20%</td>
<td data-column="Area / borough / town" data-sort-value="sutton">Sutton</td>
<td data-column="Postcode district" data-sort-value="sm6">SM6</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective grammar">selective grammar</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no new entrance exam for existing pupils">No new entrance exam for existing pupils</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds apply">Yes - sixth-form subject/GCSE thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=wallington+county+grammar+school+sm6+7ph)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Wallington+County+Grammar+School+SM6+7PH" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st dunstan&#x27;s college 46.90 48 ≥16 ≥33% lewisham se6 independent school private ~£26k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=st+dunstan%27s+college+se6+4ty)" data-state="Private" data-borough="Lewisham" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="46.9">
<td data-column="School" data-sort-value="st dunstan&#x27;s college">St Dunstan&#x27;s College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.9">46.90</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="48.0">48</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="16.0">≥16</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="33.0">≥33%</td>
<td data-column="Area / borough / town" data-sort-value="lewisham">Lewisham</td>
<td data-column="Postcode district" data-sort-value="se6">SE6</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£26k">~£26k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+dunstan%27s+college+se6+4ty)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Dunstan%27s+College+SE6+4TY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st michael&#x27;s catholic grammar school 46.84 121 24 20% barnet n12 voluntary aided state n/a selective grammar no new entrance exam for existing pupils yes - sixth-form subject/gcse thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=st+michael%27s+catholic+grammar+school+n12+7nj)" data-state="State" data-borough="Barnet" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="selective grammar" data-aps="46.84">
<td data-column="School" data-sort-value="st michael&#x27;s catholic grammar school">St Michael&#x27;s Catholic Grammar School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.84">46.84</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="121.0">121</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="24.0">24</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="20.0">20%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="n12">N12</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective grammar">selective grammar</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no new entrance exam for existing pupils">No new entrance exam for existing pupils</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds apply">Yes - sixth-form subject/GCSE thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+michael%27s+catholic+grammar+school+n12+7nj)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Michael%27s+Catholic+Grammar+School+N12+7NJ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="colfe&#x27;s school 46.71 63 ≥11 ≥17% greenwich se12 independent school private ~£26k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=colfe%27s+school+se12+8aw)" data-state="Private" data-borough="Greenwich" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="46.71">
<td data-column="School" data-sort-value="colfe&#x27;s school">Colfe&#x27;s School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.71">46.71</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="63.0">63</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="11.0">≥11</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="17.0">≥17%</td>
<td data-column="Area / borough / town" data-sort-value="greenwich">Greenwich</td>
<td data-column="Postcode district" data-sort-value="se12">SE12</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£26k">~£26k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=colfe%27s+school+se12+8aw)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Colfe%27s+School+SE12+8AW" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="francis holland school 46.67 37 ≥7 ≥19% westminster nw1 independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=francis+holland+school+nw1+6xr)" data-state="Private" data-borough="Westminster" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="46.67">
<td data-column="School" data-sort-value="francis holland school">Francis Holland School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.67">46.67</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="37.0">37</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="7.0">≥7</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="19.0">≥19%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="nw1">NW1</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=francis+holland+school+nw1+6xr)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Francis+Holland+School+NW1+6XR" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="lycee francais charles de gaulle 46.54 163 ≥12 ≥7% kensington and chelsea sw7 independent school private ~£16k-£22k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=lycee+francais+charles+de+gaulle+sw7+2dg)" data-state="Private" data-borough="Kensington and Chelsea" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="46.54">
<td data-column="School" data-sort-value="lycee francais charles de gaulle">Lycee Francais Charles de Gaulle</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.54">46.54</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="163.0">163</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="12.0">≥12</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="7.0">≥7%</td>
<td data-column="Area / borough / town" data-sort-value="kensington and chelsea">Kensington and Chelsea</td>
<td data-column="Postcode district" data-sort-value="sw7">SW7</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£16k-£22k">~£16k-£22k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=lycee+francais+charles+de+gaulle+sw7+2dg)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Lycee+Francais+Charles+de+Gaulle+SW7+2DG" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="city of london academy, highgate hill 46.00 8 ≥5 ≥62% islington n19 free school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+academy%2c+highgate+hill+n19+3eu)" data-state="State" data-borough="Islington" data-phase="secondary-only" data-school-type="Free school" data-selectivity="comprehensive/non-selective" data-aps="46.0">
<td data-column="School" data-sort-value="city of london academy, highgate hill">City of London Academy, Highgate Hill</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="46.0">46.00</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="8.0">8</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="62.0">≥62%</td>
<td data-column="Area / borough / town" data-sort-value="islington">Islington</td>
<td data-column="Postcode district" data-sort-value="n19">N19</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+academy%2c+highgate+hill+n19+3eu)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=City+of+London+Academy%2C+Highgate+Hill+N19+3EU" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="queen&#x27;s gate school 45.81 ≥28 ≥8 ≥29% kensington and chelsea sw7 independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=queen%27s+gate+school+sw7+5le)" data-state="Private" data-borough="Kensington and Chelsea" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="45.81">
<td data-column="School" data-sort-value="queen&#x27;s gate school">Queen&#x27;s Gate School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.81">45.81</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="28.0">≥28</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="29.0">≥29%</td>
<td data-column="Area / borough / town" data-sort-value="kensington and chelsea">Kensington and Chelsea</td>
<td data-column="Postcode district" data-sort-value="sw7">SW7</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=queen%27s+gate+school+sw7+5le)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Queen%27s+Gate+School+SW7+5LE" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the harrodian school 45.79 40 ≥6 ≥15% richmond upon thames sw13 independent school private ~£28k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=the+harrodian+school+sw13+9qn)" data-state="Private" data-borough="Richmond upon Thames" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="45.79">
<td data-column="School" data-sort-value="the harrodian school">The Harrodian School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.79">45.79</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="40.0">40</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="6.0">≥6</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="15.0">≥15%</td>
<td data-column="Area / borough / town" data-sort-value="richmond upon thames">Richmond upon Thames</td>
<td data-column="Postcode district" data-sort-value="sw13">SW13</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£28k">~£28k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+harrodian+school+sw13+9qn)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Harrodian+School+SW13+9QN" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="jfs 45.76 109 19 17% brent ha3 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=jfs+ha3+9te)" data-state="State" data-borough="Brent" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="45.76">
<td data-column="School" data-sort-value="jfs">JFS</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.76">45.76</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="109.0">109</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="19.0">19</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="17.0">17%</td>
<td data-column="Area / borough / town" data-sort-value="brent">Brent</td>
<td data-column="Postcode district" data-sort-value="ha3">HA3</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=jfs+ha3+9te)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=JFS+HA3+9TE" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="london academy of excellence tottenham 45.54 200 ≥35 ≥18% haringey n17 free school 16-19 state n/a selective sixth form n/a after joining; entry is at 16+ via selective sixth-form admissions yes - 16+ entry uses gcse/predicted-grade thresholds sixth-form-only [map](https://www.google.com/maps/search/?api=1&amp;query=london+academy+of+excellence+tottenham+n17+0bx)" data-state="State" data-borough="Haringey" data-phase="sixth-form-only" data-school-type="Free school 16-19" data-selectivity="selective sixth form" data-aps="45.54">
<td data-column="School" data-sort-value="london academy of excellence tottenham">London Academy of Excellence Tottenham</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.54">45.54</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="200.0">200</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="35.0">≥35</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="18.0">≥18%</td>
<td data-column="Area / borough / town" data-sort-value="haringey">Haringey</td>
<td data-column="Postcode district" data-sort-value="n17">N17</td>
<td data-column="School type" data-sort-value="free school 16-19">Free school 16-19</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective sixth form">selective sixth form</td>
<td data-column="Further exam/selection after joining?" data-sort-value="n/a after joining; entry is at 16+ via selective sixth-form admissions">N/A after joining; entry is at 16+ via selective sixth-form admissions</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - 16+ entry uses gcse/predicted-grade thresholds">Yes - 16+ entry uses GCSE/predicted-grade thresholds</td>
<td data-column="Phase" data-sort-value="sixth-form-only">sixth-form-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=london+academy+of+excellence+tottenham+n17+0bx)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=London+Academy+of+Excellence+Tottenham+N17+0BX" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the charter school north dulwich 45.19 100 25 25% southwark se24 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+charter+school+north+dulwich+se24+9jh)" data-state="State" data-borough="Southwark" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="45.19">
<td data-column="School" data-sort-value="the charter school north dulwich">The Charter School North Dulwich</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.19">45.19</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="100.0">100</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="25.0">25</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="25.0">25%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se24">SE24</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+charter+school+north+dulwich+se24+9jh)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Charter+School+North+Dulwich+SE24+9JH" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="ibstock place school 45.15 46 ≥9 ≥20% wandsworth sw15 independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=ibstock+place+school+sw15+5py)" data-state="Private" data-borough="Wandsworth" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="45.15">
<td data-column="School" data-sort-value="ibstock place school">Ibstock Place School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.15">45.15</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="46.0">46</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="20.0">≥20%</td>
<td data-column="Area / borough / town" data-sort-value="wandsworth">Wandsworth</td>
<td data-column="Postcode district" data-sort-value="sw15">SW15</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=ibstock+place+school+sw15+5py)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Ibstock+Place+School+SW15+5PY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="forest school 45.00 82 19 23% waltham forest e17 independent school private ~£25k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=forest+school+e17+3py)" data-state="Private" data-borough="Waltham Forest" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="45.0">
<td data-column="School" data-sort-value="forest school">Forest School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.0">45.00</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="82.0">82</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="19.0">19</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="23.0">23%</td>
<td data-column="Area / borough / town" data-sort-value="waltham forest">Waltham Forest</td>
<td data-column="Postcode district" data-sort-value="e17">E17</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£25k">~£25k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=forest+school+e17+3py)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Forest+School+E17+3PY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="mill hill school foundation 45.00 52 ≥9 ≥17% barnet nw7 independent school private ~£32k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=mill+hill+school+foundation+nw7+1qs)" data-state="Private" data-borough="Barnet" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="45.0">
<td data-column="School" data-sort-value="mill hill school foundation">Mill Hill School Foundation</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="45.0">45.00</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="52.0">52</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="17.0">≥17%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="nw7">NW7</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£32k">~£32k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=mill+hill+school+foundation+nw7+1qs)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Mill+Hill+School+Foundation+NW7+1QS" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st benedict&#x27;s school 44.86 48 ≥8 ≥17% ealing w5 independent school private ~£24k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=st+benedict%27s+school+w5+2es)" data-state="Private" data-borough="Ealing" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="44.86">
<td data-column="School" data-sort-value="st benedict&#x27;s school">St Benedict&#x27;s School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="44.86">44.86</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="48.0">48</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="17.0">≥17%</td>
<td data-column="Area / borough / town" data-sort-value="ealing">Ealing</td>
<td data-column="Postcode district" data-sort-value="w5">W5</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£24k">~£24k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+benedict%27s+school+w5+2es)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Benedict%27s+School+W5+2ES" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="brampton college 44.77 49 ≥10 ≥20% barnet nw4 independent school private approx. £20k-£35k; check current fee sheet academically selective/fee-paying no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed yes - course/gcse or equivalent thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=brampton+college+nw4+4dq)" data-state="Private" data-borough="Barnet" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="44.77">
<td data-column="School" data-sort-value="brampton college">Brampton College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="44.77">44.77</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="49.0">49</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="10.0">≥10</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="20.0">≥20%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="nw4">NW4</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="approx. £20k-£35k; check current fee sheet">approx. £20k-£35k; check current fee sheet</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed">No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - course/gcse or equivalent thresholds normally apply">Yes - course/GCSE or equivalent thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=brampton+college+nw4+4dq)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Brampton+College+NW4+4DQ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="blackheath high school 44.62 17 ≥5 ≥29% greenwich se3 independent school private ~£24k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=blackheath+high+school+se3+7ag)" data-state="Private" data-borough="Greenwich" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="44.62">
<td data-column="School" data-sort-value="blackheath high school">Blackheath High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="44.62">44.62</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="17.0">17</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="29.0">≥29%</td>
<td data-column="Area / borough / town" data-sort-value="greenwich">Greenwich</td>
<td data-column="Postcode district" data-sort-value="se3">SE3</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£24k">~£24k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=blackheath+high+school+se3+7ag)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Blackheath+High+School+SE3+7AG" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="west london free school 44.55 82 ≥23 ≥28% hammersmith and fulham w6 free school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=west+london+free+school+w6+9lp)" data-state="State" data-borough="Hammersmith and Fulham" data-phase="secondary-only" data-school-type="Free school" data-selectivity="comprehensive/non-selective" data-aps="44.55">
<td data-column="School" data-sort-value="west london free school">West London Free School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="44.55">44.55</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="82.0">82</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="23.0">≥23</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="28.0">≥28%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="w6">W6</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=west+london+free+school+w6+9lp)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=West+London+Free+School+W6+9LP" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="harris westminster sixth form 43.98 457 146 32% westminster sw1h free school 16-19 state n/a selective sixth form n/a after joining; entry is at 16+ via selective sixth-form admissions yes - 16+ entry uses gcse/predicted-grade thresholds sixth-form-only [map](https://www.google.com/maps/search/?api=1&amp;query=harris+westminster+sixth+form+sw1h+9lh)" data-state="State" data-borough="Westminster" data-phase="sixth-form-only" data-school-type="Free school 16-19" data-selectivity="selective sixth form" data-aps="43.98">
<td data-column="School" data-sort-value="harris westminster sixth form">Harris Westminster Sixth Form</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.98">43.98</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="457.0">457</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="146.0">146</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="32.0">32%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="sw1h">SW1H</td>
<td data-column="School type" data-sort-value="free school 16-19">Free school 16-19</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective sixth form">selective sixth form</td>
<td data-column="Further exam/selection after joining?" data-sort-value="n/a after joining; entry is at 16+ via selective sixth-form admissions">N/A after joining; entry is at 16+ via selective sixth-form admissions</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - 16+ entry uses gcse/predicted-grade thresholds">Yes - 16+ entry uses GCSE/predicted-grade thresholds</td>
<td data-column="Phase" data-sort-value="sixth-form-only">sixth-form-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=harris+westminster+sixth+form+sw1h+9lh)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Harris+Westminster+Sixth+Form+SW1H+9LH" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="woodhouse college 43.98 405 95 23% barnet n12 sixth form college state n/a sixth-form admissions criteria n/a after joining; institution starts at sixth form yes - 16+ entry uses gcse/predicted-grade/course thresholds sixth-form-only [map](https://www.google.com/maps/search/?api=1&amp;query=woodhouse+college+n12+9ey)" data-state="State" data-borough="Barnet" data-phase="sixth-form-only" data-school-type="Sixth form college" data-selectivity="sixth-form admissions criteria" data-aps="43.98">
<td data-column="School" data-sort-value="woodhouse college">Woodhouse College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.98">43.98</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="405.0">405</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="95.0">95</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="23.0">23%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="n12">N12</td>
<td data-column="School type" data-sort-value="sixth form college">Sixth form college</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="sixth-form admissions criteria">sixth-form admissions criteria</td>
<td data-column="Further exam/selection after joining?" data-sort-value="n/a after joining; institution starts at sixth form">N/A after joining; institution starts at sixth form</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - 16+ entry uses gcse/predicted-grade/course thresholds">Yes - 16+ entry uses GCSE/predicted-grade/course thresholds</td>
<td data-column="Phase" data-sort-value="sixth-form-only">sixth-form-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=woodhouse+college+n12+9ey)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Woodhouse+College+N12+9EY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="hasmonean high school for girls 43.66 ≥16 ≥5 ≥31% barnet nw7 academy state n/a not listed as academically selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=hasmonean+high+school+for+girls+nw7+2eu)" data-state="State" data-borough="Barnet" data-phase="secondary-only" data-school-type="Academy" data-selectivity="not listed as academically selective" data-aps="43.66">
<td data-column="School" data-sort-value="hasmonean high school for girls">Hasmonean High School for Girls</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.66">43.66</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="16.0">≥16</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="31.0">≥31%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="nw7">NW7</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="not listed as academically selective">not listed as academically selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=hasmonean+high+school+for+girls+nw7+2eu)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Hasmonean+High+School+for+Girls+NW7+2EU" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the king alfred school 43.65 ≥13 ≥0 ≥0% barnet nw11 independent school private ~£25k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=the+king+alfred+school+nw11+7hy)" data-state="Private" data-borough="Barnet" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="43.65">
<td data-column="School" data-sort-value="the king alfred school">The King Alfred School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.65">43.65</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="13.0">≥13</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="nw11">NW11</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£25k">~£25k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+king+alfred+school+nw11+7hy)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+King+Alfred+School+NW11+7HY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the camden school for girls 43.54 173 68 39% camden nw5 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+camden+school+for+girls+nw5+2db)" data-state="State" data-borough="Camden" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="43.54">
<td data-column="School" data-sort-value="the camden school for girls">The Camden School for Girls</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.54">43.54</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="173.0">173</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="68.0">68</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="39.0">39%</td>
<td data-column="Area / borough / town" data-sort-value="camden">Camden</td>
<td data-column="Postcode district" data-sort-value="nw5">NW5</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+camden+school+for+girls+nw5+2db)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Camden+School+for+Girls+NW5+2DB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="twyford church of england high school 43.51 151 38 25% ealing w3 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=twyford+church+of+england+high+school+w3+9pp)" data-state="State" data-borough="Ealing" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="43.51">
<td data-column="School" data-sort-value="twyford church of england high school">Twyford Church of England High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.51">43.51</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="151.0">151</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="38.0">38</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="25.0">25%</td>
<td data-column="Area / borough / town" data-sort-value="ealing">Ealing</td>
<td data-column="Postcode district" data-sort-value="w3">W3</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=twyford+church+of+england+high+school+w3+9pp)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Twyford+Church+of+England+High+School+W3+9PP" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the totteridge academy 43.47 ≥6 ≥5 ≥83% barnet n20 academy state n/a not listed as academically selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+totteridge+academy+n20+8az)" data-state="State" data-borough="Barnet" data-phase="secondary-only" data-school-type="Academy" data-selectivity="not listed as academically selective" data-aps="43.47">
<td data-column="School" data-sort-value="the totteridge academy">The Totteridge Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.47">43.47</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="6.0">≥6</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="83.0">≥83%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="n20">N20</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="not listed as academically selective">not listed as academically selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+totteridge+academy+n20+8az)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Totteridge+Academy+N20+8AZ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the london oratory school 43.27 161 38 24% hammersmith and fulham sw6 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=the+london+oratory+school+sw6+1rx)" data-state="State" data-borough="Hammersmith and Fulham" data-phase="partial all-through" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="43.27">
<td data-column="School" data-sort-value="the london oratory school">The London Oratory School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.27">43.27</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="161.0">161</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="38.0">38</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="24.0">24%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="sw6">SW6</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+london+oratory+school+sw6+1rx)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+London+Oratory+School+SW6+1RX" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="mossbourne community academy 43.22 131 45 34% hackney e5 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=mossbourne+community+academy+e5+8jy)" data-state="State" data-borough="Hackney" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="43.22">
<td data-column="School" data-sort-value="mossbourne community academy">Mossbourne Community Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.22">43.22</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="131.0">131</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="45.0">45</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="34.0">34%</td>
<td data-column="Area / borough / town" data-sort-value="hackney">Hackney</td>
<td data-column="Postcode district" data-sort-value="e5">E5</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=mossbourne+community+academy+e5+8jy)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Mossbourne+Community+Academy+E5+8JY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="menorah high school for girls 43.13 ≥0 ≥0 0% brent nw2 voluntary aided state n/a not listed as academically selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=menorah+high+school+for+girls+nw2+7bz)" data-state="State" data-borough="Brent" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="not listed as academically selective" data-aps="43.13">
<td data-column="School" data-sort-value="menorah high school for girls">Menorah High School for Girls</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="43.13">43.13</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">0%</td>
<td data-column="Area / borough / town" data-sort-value="brent">Brent</td>
<td data-column="Postcode district" data-sort-value="nw2">NW2</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="not listed as academically selective">not listed as academically selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=menorah+high+school+for+girls+nw2+7bz)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Menorah+High+School+for+Girls+NW2+7BZ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st james senior girls&#x27; school 42.96 ≥13 ≥4 ≥31% hammersmith and fulham w14 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=st+james+senior+girls%27+school+w14+8sh)" data-state="Private" data-borough="Hammersmith and Fulham" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="42.96">
<td data-column="School" data-sort-value="st james senior girls&#x27; school">St James Senior Girls&#x27; School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="42.96">42.96</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="13.0">≥13</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="4.0">≥4</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="31.0">≥31%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="w14">W14</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+james+senior+girls%27+school+w14+8sh)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+James+Senior+Girls%27+School+W14+8SH" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="beth jacob grammar school for girls 42.75 0 0 0% barnet nw4 independent school private see school academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds 11 to 17 [map](https://www.google.com/maps/search/?api=1&amp;query=beth+jacob+grammar+school+for+girls+nw4+2at)" data-state="Private" data-borough="Barnet" data-phase="11 to 17" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="42.75">
<td data-column="School" data-sort-value="beth jacob grammar school for girls">Beth Jacob Grammar School for Girls</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="42.75">42.75</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="0.0">0</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">0%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="nw4">NW4</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="see school">see school</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="11 to 17">11 to 17</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=beth+jacob+grammar+school+for+girls+nw4+2at)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Beth+Jacob+Grammar+School+for+Girls+NW4+2AT" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the cardinal vaughan memorial rc school 42.67 136 37 27% kensington and chelsea w14 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+cardinal+vaughan+memorial+rc+school+w14+8bz)" data-state="State" data-borough="Kensington and Chelsea" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="42.67">
<td data-column="School" data-sort-value="the cardinal vaughan memorial rc school">The Cardinal Vaughan Memorial RC School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="42.67">42.67</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="136.0">136</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="37.0">37</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="27.0">27%</td>
<td data-column="Area / borough / town" data-sort-value="kensington and chelsea">Kensington and Chelsea</td>
<td data-column="Postcode district" data-sort-value="w14">W14</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+cardinal+vaughan+memorial+rc+school+w14+8bz)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Cardinal+Vaughan+Memorial+RC+School+W14+8BZ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="woodford county high school 42.59 76 25 33% waltham forest ig8 community school state n/a selective grammar no new entrance exam for existing pupils yes - sixth-form subject/gcse thresholds apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=woodford+county+high+school+ig8+9la)" data-state="State" data-borough="Waltham Forest" data-phase="secondary-only" data-school-type="Community school" data-selectivity="selective grammar" data-aps="42.59">
<td data-column="School" data-sort-value="woodford county high school">Woodford County High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="42.59">42.59</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="76.0">76</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="25.0">25</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="33.0">33%</td>
<td data-column="Area / borough / town" data-sort-value="waltham forest">Waltham Forest</td>
<td data-column="Postcode district" data-sort-value="ig8">IG8</td>
<td data-column="School type" data-sort-value="community school">Community school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="selective grammar">selective grammar</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no new entrance exam for existing pupils">No new entrance exam for existing pupils</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds apply">Yes - sixth-form subject/GCSE thresholds apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=woodford+county+high+school+ig8+9la)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Woodford+County+High+School+IG8+9LA" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the st marylebone cofe school 42.22 117 ≥24 ≥21% westminster w1u academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+st+marylebone+cofe+school+w1u+5ba)" data-state="State" data-borough="Westminster" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="42.22">
<td data-column="School" data-sort-value="the st marylebone cofe school">The St Marylebone CofE School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="42.22">42.22</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="117.0">117</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="24.0">≥24</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="21.0">≥21%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="w1u">W1U</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+st+marylebone+cofe+school+w1u+5ba)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+St+Marylebone+CofE+School+W1U+5BA" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="ashcroft technology academy 42.03 97 ≥10 ≥10% wandsworth sw15 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=ashcroft+technology+academy+sw15+2ut)" data-state="State" data-borough="Wandsworth" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="42.03">
<td data-column="School" data-sort-value="ashcroft technology academy">Ashcroft Technology Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="42.03">42.03</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="97.0">97</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="10.0">≥10</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="10.0">≥10%</td>
<td data-column="Area / borough / town" data-sort-value="wandsworth">Wandsworth</td>
<td data-column="Postcode district" data-sort-value="sw15">SW15</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=ashcroft+technology+academy+sw15+2ut)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Ashcroft+Technology+Academy+SW15+2UT" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="radnor house 41.85 ≥11 ≥0 ≥0% richmond upon thames tw1 independent school private ~£25k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=radnor+house+tw1+4qg)" data-state="Private" data-borough="Richmond upon Thames" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="41.85">
<td data-column="School" data-sort-value="radnor house">Radnor House</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.85">41.85</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="11.0">≥11</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="richmond upon thames">Richmond upon Thames</td>
<td data-column="Postcode district" data-sort-value="tw1">TW1</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£25k">~£25k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=radnor+house+tw1+4qg)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Radnor+House+TW1+4QG" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the st thomas the apostle college 41.79 54 ≥9 ≥17% southwark se15 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+st+thomas+the+apostle+college+se15+2eb)" data-state="State" data-borough="Southwark" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="41.79">
<td data-column="School" data-sort-value="the st thomas the apostle college">The St Thomas the Apostle College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.79">41.79</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="54.0">54</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="17.0">≥17%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se15">SE15</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+st+thomas+the+apostle+college+se15+2eb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+St+Thomas+the+Apostle+College+SE15+2EB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="streatham &amp; clapham high school 41.69 ≥19 ≥9 ≥47% lambeth sw16 independent school private ~£24k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=streatham+%26+clapham+high+school+sw16+1aw)" data-state="Private" data-borough="Lambeth" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="41.69">
<td data-column="School" data-sort-value="streatham &amp; clapham high school">Streatham &amp; Clapham High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.69">41.69</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="19.0">≥19</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="47.0">≥47%</td>
<td data-column="Area / borough / town" data-sort-value="lambeth">Lambeth</td>
<td data-column="Postcode district" data-sort-value="sw16">SW16</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£24k">~£24k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=streatham+%26+clapham+high+school+sw16+1aw)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Streatham+%26+Clapham+High+School+SW16+1AW" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="wetherby senior school 41.50 26 ≥0 ≥0% westminster w1u independent school private ~£29k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=wetherby+senior+school+w1u+2qu)" data-state="Private" data-borough="Westminster" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="41.5">
<td data-column="School" data-sort-value="wetherby senior school">Wetherby Senior School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.5">41.50</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="26.0">26</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="w1u">W1U</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£29k">~£29k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=wetherby+senior+school+w1u+2qu)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Wetherby+Senior+School+W1U+2QU" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st catherine&#x27;s school 41.48 ≥8 ≥0 ≥0% richmond upon thames tw1 independent school private approx. £20k-£35k; check current fee sheet academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=st+catherine%27s+school+tw1+4qj)" data-state="Private" data-borough="Richmond upon Thames" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="41.48">
<td data-column="School" data-sort-value="st catherine&#x27;s school">St Catherine&#x27;s School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.48">41.48</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="richmond upon thames">Richmond upon Thames</td>
<td data-column="Postcode district" data-sort-value="tw1">TW1</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="approx. £20k-£35k; check current fee sheet">approx. £20k-£35k; check current fee sheet</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+catherine%27s+school+tw1+4qj)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Catherine%27s+School+TW1+4QJ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="lady margaret school 41.44 42 ≥13 ≥31% hammersmith and fulham sw6 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=lady+margaret+school+sw6+4un)" data-state="State" data-borough="Hammersmith and Fulham" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="41.44">
<td data-column="School" data-sort-value="lady margaret school">Lady Margaret School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.44">41.44</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="42.0">42</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="13.0">≥13</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="31.0">≥31%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="sw6">SW6</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=lady+margaret+school+sw6+4un)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Lady+Margaret+School+SW6+4UN" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="sydenham high school, gdst 41.37 ≥17 ≥0 ≥0% lewisham se26 independent school private ~£23k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=sydenham+high+school%2c+gdst+se26+6bl)" data-state="Private" data-borough="Lewisham" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="41.37">
<td data-column="School" data-sort-value="sydenham high school, gdst">Sydenham High School, GDST</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.37">41.37</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="17.0">≥17</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="lewisham">Lewisham</td>
<td data-column="Postcode district" data-sort-value="se26">SE26</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£23k">~£23k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=sydenham+high+school%2c+gdst+se26+6bl)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Sydenham+High+School%2C+GDST+SE26+6BL" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="paddington academy 41.32 35 ≥8 ≥23% westminster w9 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=paddington+academy+w9+2dr)" data-state="State" data-borough="Westminster" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="41.32">
<td data-column="School" data-sort-value="paddington academy">Paddington Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.32">41.32</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="35.0">35</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="23.0">≥23%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="w9">W9</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=paddington+academy+w9+2dr)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Paddington+Academy+W9+2DR" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="holland park school 41.31 58 ≥16 ≥28% kensington and chelsea w8 academy state n/a not listed as academically selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=holland+park+school+w8+7af)" data-state="State" data-borough="Kensington and Chelsea" data-phase="secondary-only" data-school-type="Academy" data-selectivity="not listed as academically selective" data-aps="41.31">
<td data-column="School" data-sort-value="holland park school">Holland Park School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="41.31">41.31</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="58.0">58</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="16.0">≥16</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="28.0">≥28%</td>
<td data-column="Area / borough / town" data-sort-value="kensington and chelsea">Kensington and Chelsea</td>
<td data-column="Postcode district" data-sort-value="w8">W8</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="not listed as academically selective">not listed as academically selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=holland+park+school+w8+7af)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Holland+Park+School+W8+7AF" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="guildhouse school 40.86 ≥9 ≥0 ≥0% camden wc1a independent school private ~£30k academically selective/fee-paying no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed yes - course/gcse or equivalent thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=guildhouse+school+wc1a+2ra)" data-state="Private" data-borough="Camden" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="40.86">
<td data-column="School" data-sort-value="guildhouse school">Guildhouse School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.86">40.86</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="camden">Camden</td>
<td data-column="Postcode district" data-sort-value="wc1a">WC1A</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£30k">~£30k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed">No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - course/gcse or equivalent thresholds normally apply">Yes - course/GCSE or equivalent thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=guildhouse+school+wc1a+2ra)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Guildhouse+School+WC1A+2RA" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st mark&#x27;s church of england academy 40.44 ≥8 ≥0 ≥0% merton cr4 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=st+mark%27s+church+of+england+academy+cr4+1sf)" data-state="State" data-borough="Merton" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="40.44">
<td data-column="School" data-sort-value="st mark&#x27;s church of england academy">St Mark&#x27;s Church of England Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.44">40.44</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="merton">Merton</td>
<td data-column="Postcode district" data-sort-value="cr4">CR4</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+mark%27s+church+of+england+academy+cr4+1sf)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Mark%27s+Church+of+England+Academy+CR4+1SF" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="ashbourne college 40.42 49 ≥9 ≥18% kensington and chelsea w8 independent school private ~£33k academically selective/fee-paying no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed yes - course/gcse or equivalent thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=ashbourne+college+w8+4pl)" data-state="Private" data-borough="Kensington and Chelsea" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="40.42">
<td data-column="School" data-sort-value="ashbourne college">Ashbourne College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.42">40.42</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="49.0">49</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="18.0">≥18%</td>
<td data-column="Area / borough / town" data-sort-value="kensington and chelsea">Kensington and Chelsea</td>
<td data-column="Postcode district" data-sort-value="w8">W8</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£33k">~£33k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed">No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - course/gcse or equivalent thresholds normally apply">Yes - course/GCSE or equivalent thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=ashbourne+college+w8+4pl)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Ashbourne+College+W8+4PL" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="lubavitch house school (senior girls) 40.30 0 0 0% hackney n16 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=lubavitch+house+school+%28senior+girls%29+n16+5rp)" data-state="State" data-borough="Hackney" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="40.3">
<td data-column="School" data-sort-value="lubavitch house school (senior girls)">Lubavitch House School (Senior Girls)</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.3">40.30</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="0.0">0</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">0%</td>
<td data-column="Area / borough / town" data-sort-value="hackney">Hackney</td>
<td data-column="Postcode district" data-sort-value="n16">N16</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=lubavitch+house+school+%28senior+girls%29+n16+5rp)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Lubavitch+House+School+%28Senior+Girls%29+N16+5RP" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="mander portman woodward school 40.27 66 ≥12 ≥18% kensington and chelsea sw7 independent school private ~£34k academically selective/fee-paying no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed yes - course/gcse or equivalent thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=mander+portman+woodward+school+sw7+5ab)" data-state="Private" data-borough="Kensington and Chelsea" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="40.27">
<td data-column="School" data-sort-value="mander portman woodward school">Mander Portman Woodward School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.27">40.27</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="66.0">66</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="12.0">≥12</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="18.0">≥18%</td>
<td data-column="Area / borough / town" data-sort-value="kensington and chelsea">Kensington and Chelsea</td>
<td data-column="Postcode district" data-sort-value="sw7">SW7</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£34k">~£34k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed">No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - course/gcse or equivalent thresholds normally apply">Yes - course/GCSE or equivalent thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=mander+portman+woodward+school+sw7+5ab)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Mander+Portman+Woodward+School+SW7+5AB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="old palace of john whitgift school 40.23 45 ≥3 ≥7% croydon cr0 independent school private ~£22k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds partial all-through [map](https://www.google.com/maps/search/?api=1&amp;query=old+palace+of+john+whitgift+school+cr0+1ax)" data-state="Private" data-borough="Croydon" data-phase="partial all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="40.23">
<td data-column="School" data-sort-value="old palace of john whitgift school">Old Palace of John Whitgift School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.23">40.23</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="45.0">45</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="3.0">≥3</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="7.0">≥7%</td>
<td data-column="Area / borough / town" data-sort-value="croydon">Croydon</td>
<td data-column="Postcode district" data-sort-value="cr0">CR0</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£22k">~£22k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="partial all-through">partial all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=old+palace+of+john+whitgift+school+cr0+1ax)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Old+Palace+of+John+Whitgift+School+CR0+1AX" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the grey coat hospital 40.20 75 ≥23 ≥31% westminster sw1p academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+grey+coat+hospital+sw1p+2dy)" data-state="State" data-borough="Westminster" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="40.2">
<td data-column="School" data-sort-value="the grey coat hospital">The Grey Coat Hospital</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.2">40.20</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="75.0">75</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="23.0">≥23</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="31.0">≥31%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="sw1p">SW1P</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+grey+coat+hospital+sw1p+2dy)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Grey+Coat+Hospital+SW1P+2DY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="kingsdale foundation school 40.11 62 25 40% southwark se21 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=kingsdale+foundation+school+se21+8sq)" data-state="State" data-borough="Southwark" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="40.11">
<td data-column="School" data-sort-value="kingsdale foundation school">Kingsdale Foundation School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.11">40.11</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="62.0">62</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="25.0">25</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="40.0">40%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se21">SE21</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=kingsdale+foundation+school+se21+8sq)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Kingsdale+Foundation+School+SE21+8SQ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the elms academy 40.00 ≥24 ≥8 ≥33% lambeth sw4 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+elms+academy+sw4+9et)" data-state="State" data-borough="Lambeth" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="40.0">
<td data-column="School" data-sort-value="the elms academy">The Elms Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="40.0">40.00</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="24.0">≥24</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="33.0">≥33%</td>
<td data-column="Area / borough / town" data-sort-value="lambeth">Lambeth</td>
<td data-column="Postcode district" data-sort-value="sw4">SW4</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+elms+academy+sw4+9et)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Elms+Academy+SW4+9ET" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st mary magdalene academy 39.96 84 ≥17 ≥20% islington n7 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply all-through [map](https://www.google.com/maps/search/?api=1&amp;query=st+mary+magdalene+academy+n7+8pg)" data-state="State" data-borough="Islington" data-phase="all-through" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="39.96">
<td data-column="School" data-sort-value="st mary magdalene academy">St Mary Magdalene Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.96">39.96</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="84.0">84</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="17.0">≥17</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="20.0">≥20%</td>
<td data-column="Area / borough / town" data-sort-value="islington">Islington</td>
<td data-column="Postcode district" data-sort-value="n7">N7</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+mary+magdalene+academy+n7+8pg)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Mary+Magdalene+Academy+N7+8PG" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="artsed day school &amp; sixth form 39.95 ≥3 ≥0 ≥0% hounslow w4 independent school private ~£25k academically selective/fee-paying no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed yes - course/gcse or equivalent thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=artsed+day+school+%26+sixth+form+w4+1ly)" data-state="Private" data-borough="Hounslow" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="39.95">
<td data-column="School" data-sort-value="artsed day school &amp; sixth form">ArtsEd Day School &amp; Sixth Form</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.95">39.95</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="3.0">≥3</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="hounslow">Hounslow</td>
<td data-column="Postcode district" data-sort-value="w4">W4</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£25k">~£25k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed">No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - course/gcse or equivalent thresholds normally apply">Yes - course/GCSE or equivalent thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=artsed+day+school+%26+sixth+form+w4+1ly)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=ArtsEd+Day+School+%26+Sixth+Form+W4+1LY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="gunnersbury catholic school 39.92 28 ≥0 ≥0% hounslow tw8 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=gunnersbury+catholic+school+tw8+9lb)" data-state="State" data-borough="Hounslow" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="39.92">
<td data-column="School" data-sort-value="gunnersbury catholic school">Gunnersbury Catholic School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.92">39.92</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="28.0">28</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="hounslow">Hounslow</td>
<td data-column="Postcode district" data-sort-value="tw8">TW8</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=gunnersbury+catholic+school+tw8+9lb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Gunnersbury+Catholic+School+TW8+9LB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="ark globe academy 39.51 27 ≥8 ≥30% southwark se1 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply all-through [map](https://www.google.com/maps/search/?api=1&amp;query=ark+globe+academy+se1+6ag)" data-state="State" data-borough="Southwark" data-phase="all-through" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="39.51">
<td data-column="School" data-sort-value="ark globe academy">Ark Globe Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.51">39.51</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="27.0">27</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="30.0">≥30%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se1">SE1</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=ark+globe+academy+se1+6ag)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Ark+Globe+Academy+SE1+6AG" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="hasmonean high school for boys 39.41 23 ≥12 ≥52% barnet nw4 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=hasmonean+high+school+for+boys+nw4+1na)" data-state="State" data-borough="Barnet" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="39.41">
<td data-column="School" data-sort-value="hasmonean high school for boys">Hasmonean High School for Boys</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.41">39.41</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="23.0">23</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="12.0">≥12</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="52.0">≥52%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="nw4">NW4</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=hasmonean+high+school+for+boys+nw4+1na)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Hasmonean+High+School+for+Boys+NW4+1NA" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="city of london academy, shoreditch park 39.34 ≥6 ≥5 ≥83% hackney n1 free school state n/a not listed as academically selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+academy%2c+shoreditch+park+n1+5ju)" data-state="State" data-borough="Hackney" data-phase="secondary-only" data-school-type="Free school" data-selectivity="not listed as academically selective" data-aps="39.34">
<td data-column="School" data-sort-value="city of london academy, shoreditch park">City of London Academy, Shoreditch Park</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.34">39.34</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="6.0">≥6</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="83.0">≥83%</td>
<td data-column="Area / borough / town" data-sort-value="hackney">Hackney</td>
<td data-column="Postcode district" data-sort-value="n1">N1</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="not listed as academically selective">not listed as academically selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=city+of+london+academy%2c+shoreditch+park+n1+5ju)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=City+of+London+Academy%2C+Shoreditch+Park+N1+5JU" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="prendergast school 39.34 39 ≥9 ≥23% lewisham se4 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=prendergast+school+se4+1le)" data-state="State" data-borough="Lewisham" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="39.34">
<td data-column="School" data-sort-value="prendergast school">Prendergast School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.34">39.34</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="39.0">39</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="23.0">≥23%</td>
<td data-column="Area / borough / town" data-sort-value="lewisham">Lewisham</td>
<td data-column="Postcode district" data-sort-value="se4">SE4</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=prendergast+school+se4+1le)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Prendergast+School+SE4+1LE" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="babington house school 39.33 ≥5 ≥0 ≥0% bromley br7 independent school private ~£22k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds all-through [map](https://www.google.com/maps/search/?api=1&amp;query=babington+house+school+br7+5es)" data-state="Private" data-borough="Bromley" data-phase="all-through" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="39.33">
<td data-column="School" data-sort-value="babington house school">Babington House School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.33">39.33</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="bromley">Bromley</td>
<td data-column="Postcode district" data-sort-value="br7">BR7</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£22k">~£22k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=babington+house+school+br7+5es)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Babington+House+School+BR7+5ES" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st gregory&#x27;s catholic science college 39.14 ≥14 ≥0 ≥0% brent ha3 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=st+gregory%27s+catholic+science+college+ha3+0nb)" data-state="State" data-borough="Brent" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="39.14">
<td data-column="School" data-sort-value="st gregory&#x27;s catholic science college">St Gregory&#x27;s Catholic Science College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="39.14">39.14</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="14.0">≥14</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="brent">Brent</td>
<td data-column="Postcode district" data-sort-value="ha3">HA3</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+gregory%27s+catholic+science+college+ha3+0nb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Gregory%27s+Catholic+Science+College+HA3+0NB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="bishop thomas grant catholic secondary school 38.89 37 ≥8 ≥22% lambeth sw16 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=bishop+thomas+grant+catholic+secondary+school+sw16+2hy)" data-state="State" data-borough="Lambeth" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="38.89">
<td data-column="School" data-sort-value="bishop thomas grant catholic secondary school">Bishop Thomas Grant Catholic Secondary School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.89">38.89</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="37.0">37</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="22.0">≥22%</td>
<td data-column="Area / borough / town" data-sort-value="lambeth">Lambeth</td>
<td data-column="Postcode district" data-sort-value="sw16">SW16</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=bishop+thomas+grant+catholic+secondary+school+sw16+2hy)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Bishop+Thomas+Grant+Catholic+Secondary+School+SW16+2HY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the fulham boys school 38.86 30 ≥11 ≥37% hammersmith and fulham sw6 free school state n/a not listed as academically selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+fulham+boys+school+sw6+5bd)" data-state="State" data-borough="Hammersmith and Fulham" data-phase="secondary-only" data-school-type="Free school" data-selectivity="not listed as academically selective" data-aps="38.86">
<td data-column="School" data-sort-value="the fulham boys school">The Fulham Boys School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.86">38.86</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="30.0">30</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="11.0">≥11</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="37.0">≥37%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="sw6">SW6</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="not listed as academically selective">not listed as academically selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+fulham+boys+school+sw6+5bd)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Fulham+Boys+School+SW6+5BD" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="north bridge house senior canonbury school 38.85 ≥5 ≥0 ≥0% islington n1 independent school private ~£27k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=north+bridge+house+senior+canonbury+school+n1+2nq)" data-state="Private" data-borough="Islington" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="38.85">
<td data-column="School" data-sort-value="north bridge house senior canonbury school">North Bridge House Senior Canonbury School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.85">38.85</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="islington">Islington</td>
<td data-column="Postcode district" data-sort-value="n1">N1</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£27k">~£27k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=north+bridge+house+senior+canonbury+school+n1+2nq)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=North+Bridge+House+Senior+Canonbury+School+N1+2NQ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="grey court school 38.84 51 ≥5 ≥10% richmond upon thames tw10 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=grey+court+school+tw10+7hn)" data-state="State" data-borough="Richmond upon Thames" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="38.84">
<td data-column="School" data-sort-value="grey court school">Grey Court School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.84">38.84</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="51.0">51</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="10.0">≥10%</td>
<td data-column="Area / borough / town" data-sort-value="richmond upon thames">Richmond upon Thames</td>
<td data-column="Postcode district" data-sort-value="tw10">TW10</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=grey+court+school+tw10+7hn)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Grey+Court+School+TW10+7HN" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="ark bolingbroke academy 38.82 34 ≥4 ≥12% wandsworth sw11 free school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=ark+bolingbroke+academy+sw11+6bf)" data-state="State" data-borough="Wandsworth" data-phase="secondary-only" data-school-type="Free school" data-selectivity="comprehensive/non-selective" data-aps="38.82">
<td data-column="School" data-sort-value="ark bolingbroke academy">Ark Bolingbroke Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.82">38.82</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="34.0">34</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="4.0">≥4</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="12.0">≥12%</td>
<td data-column="Area / borough / town" data-sort-value="wandsworth">Wandsworth</td>
<td data-column="Postcode district" data-sort-value="sw11">SW11</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=ark+bolingbroke+academy+sw11+6bf)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Ark+Bolingbroke+Academy+SW11+6BF" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="highlands school 38.82 ≥21 ≥0 ≥0% enfield n21 community school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=highlands+school+n21+1qq)" data-state="State" data-borough="Enfield" data-phase="secondary-only" data-school-type="Community school" data-selectivity="comprehensive/non-selective" data-aps="38.82">
<td data-column="School" data-sort-value="highlands school">Highlands School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.82">38.82</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="21.0">≥21</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="enfield">Enfield</td>
<td data-column="Postcode district" data-sort-value="n21">N21</td>
<td data-column="School type" data-sort-value="community school">Community school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=highlands+school+n21+1qq)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Highlands+School+N21+1QQ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="glenthorne high school 38.72 46 ≥5 ≥11% sutton sm3 academy state n/a non-selective in selective area no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=glenthorne+high+school+sm3+9ps)" data-state="State" data-borough="Sutton" data-phase="secondary-only" data-school-type="Academy" data-selectivity="non-selective in selective area" data-aps="38.72">
<td data-column="School" data-sort-value="glenthorne high school">Glenthorne High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.72">38.72</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="46.0">46</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="11.0">≥11%</td>
<td data-column="Area / borough / town" data-sort-value="sutton">Sutton</td>
<td data-column="Postcode district" data-sort-value="sm3">SM3</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="non-selective in selective area">non-selective in selective area</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=glenthorne+high+school+sm3+9ps)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Glenthorne+High+School+SM3+9PS" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="the kingston academy 38.64 ≥27 ≥10 ≥37% kingston upon thames kt2 free school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=the+kingston+academy+kt2+5pe)" data-state="State" data-borough="Kingston upon Thames" data-phase="secondary-only" data-school-type="Free school" data-selectivity="comprehensive/non-selective" data-aps="38.64">
<td data-column="School" data-sort-value="the kingston academy">The Kingston Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.64">38.64</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="27.0">≥27</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="10.0">≥10</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="37.0">≥37%</td>
<td data-column="Area / borough / town" data-sort-value="kingston upon thames">Kingston upon Thames</td>
<td data-column="Postcode district" data-sort-value="kt2">KT2</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=the+kingston+academy+kt2+5pe)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=The+Kingston+Academy+KT2+5PE" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="central foundation boys&#x27; school 38.47 29 ≥5 ≥17% islington ec2a voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=central+foundation+boys%27+school+ec2a+4sh)" data-state="State" data-borough="Islington" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="38.47">
<td data-column="School" data-sort-value="central foundation boys&#x27; school">Central Foundation Boys&#x27; School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.47">38.47</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="29.0">29</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="17.0">≥17%</td>
<td data-column="Area / borough / town" data-sort-value="islington">Islington</td>
<td data-column="Postcode district" data-sort-value="ec2a">EC2A</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=central+foundation+boys%27+school+ec2a+4sh)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Central+Foundation+Boys%27+School+EC2A+4SH" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="kensington aldridge academy 38.46 50 ≥4 ≥8% kensington and chelsea w10 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=kensington+aldridge+academy+w10+6ex)" data-state="State" data-borough="Kensington and Chelsea" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="38.46">
<td data-column="School" data-sort-value="kensington aldridge academy">Kensington Aldridge Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.46">38.46</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="50.0">50</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="4.0">≥4</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="8.0">≥8%</td>
<td data-column="Area / borough / town" data-sort-value="kensington and chelsea">Kensington and Chelsea</td>
<td data-column="Postcode district" data-sort-value="w10">W10</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=kensington+aldridge+academy+w10+6ex)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Kensington+Aldridge+Academy+W10+6EX" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="ark academy 38.39 37 ≥11 ≥30% brent ha9 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply all-through [map](https://www.google.com/maps/search/?api=1&amp;query=ark+academy+ha9+9jr)" data-state="State" data-borough="Brent" data-phase="all-through" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="38.39">
<td data-column="School" data-sort-value="ark academy">Ark Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.39">38.39</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="37.0">37</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="11.0">≥11</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="30.0">≥30%</td>
<td data-column="Area / borough / town" data-sort-value="brent">Brent</td>
<td data-column="Postcode district" data-sort-value="ha9">HA9</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=ark+academy+ha9+9jr)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Ark+Academy+HA9+9JR" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="parliament hill school 38.39 5 0 0% camden nw5 community school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=parliament+hill+school+nw5+1rl)" data-state="State" data-borough="Camden" data-phase="secondary-only" data-school-type="Community school" data-selectivity="comprehensive/non-selective" data-aps="38.39">
<td data-column="School" data-sort-value="parliament hill school">Parliament Hill School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.39">38.39</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="5.0">5</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">0%</td>
<td data-column="Area / borough / town" data-sort-value="camden">Camden</td>
<td data-column="Postcode district" data-sort-value="nw5">NW5</td>
<td data-column="School type" data-sort-value="community school">Community school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=parliament+hill+school+nw5+1rl)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Parliament+Hill+School+NW5+1RL" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="orleans park school 38.29 34 ≥5 ≥15% richmond upon thames tw1 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=orleans+park+school+tw1+3bb)" data-state="State" data-borough="Richmond upon Thames" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="38.29">
<td data-column="School" data-sort-value="orleans park school">Orleans Park School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.29">38.29</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="34.0">34</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="15.0">≥15%</td>
<td data-column="Area / borough / town" data-sort-value="richmond upon thames">Richmond upon Thames</td>
<td data-column="Postcode district" data-sort-value="tw1">TW1</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=orleans+park+school+tw1+3bb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Orleans+Park+School+TW1+3BB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="ashmole academy 38.25 85 ≥18 ≥21% barnet n14 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=ashmole+academy+n14+5rj)" data-state="State" data-borough="Barnet" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="38.25">
<td data-column="School" data-sort-value="ashmole academy">Ashmole Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.25">38.25</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="85.0">85</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="18.0">≥18</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="21.0">≥21%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="n14">N14</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=ashmole+academy+n14+5rj)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Ashmole+Academy+N14+5RJ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="fine arts college 38.22 ≥10 ≥0 ≥0% camden nw3 independent school private ~£34k academically selective/fee-paying no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed yes - course/gcse or equivalent thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=fine+arts+college+nw3+4yd)" data-state="Private" data-borough="Camden" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="38.22">
<td data-column="School" data-sort-value="fine arts college">Fine Arts College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.22">38.22</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="10.0">≥10</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="camden">Camden</td>
<td data-column="Postcode district" data-sort-value="nw3">NW3</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£34k">~£34k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no internal re-entry exam noted; external 16+ applicants may be assessed/interviewed">No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - course/gcse or equivalent thresholds normally apply">Yes - course/GCSE or equivalent thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=fine+arts+college+nw3+4yd)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Fine+Arts+College+NW3+4YD" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="greenshaw high school 38.20 36 ≥11 ≥31% sutton sm1 academy state n/a non-selective in selective area no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=greenshaw+high+school+sm1+3dy)" data-state="State" data-borough="Sutton" data-phase="secondary-only" data-school-type="Academy" data-selectivity="non-selective in selective area" data-aps="38.2">
<td data-column="School" data-sort-value="greenshaw high school">Greenshaw High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.2">38.20</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="36.0">36</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="11.0">≥11</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="31.0">≥31%</td>
<td data-column="Area / borough / town" data-sort-value="sutton">Sutton</td>
<td data-column="Postcode district" data-sort-value="sm1">SM1</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="non-selective in selective area">non-selective in selective area</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=greenshaw+high+school+sm1+3dy)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Greenshaw+High+School+SM1+3DY" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="william perkin church of england high school 38.13 ≥42 ≥5 ≥12% ealing ub6 free school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=william+perkin+church+of+england+high+school+ub6+8pr)" data-state="State" data-borough="Ealing" data-phase="secondary-only" data-school-type="Free school" data-selectivity="comprehensive/non-selective" data-aps="38.13">
<td data-column="School" data-sort-value="william perkin church of england high school">William Perkin Church of England High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="38.13">38.13</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="42.0">≥42</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="12.0">≥12%</td>
<td data-column="Area / borough / town" data-sort-value="ealing">Ealing</td>
<td data-column="Postcode district" data-sort-value="ub6">UB6</td>
<td data-column="School type" data-sort-value="free school">Free school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=william+perkin+church+of+england+high+school+ub6+8pr)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=William+Perkin+Church+of+England+High+School+UB6+8PR" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="alexandra park school 37.74 61 18 30% haringey n11 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=alexandra+park+school+n11+2az)" data-state="State" data-borough="Haringey" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.74">
<td data-column="School" data-sort-value="alexandra park school">Alexandra Park School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.74">37.74</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="61.0">61</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="18.0">18</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="30.0">30%</td>
<td data-column="Area / borough / town" data-sort-value="haringey">Haringey</td>
<td data-column="Postcode district" data-sort-value="n11">N11</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=alexandra+park+school+n11+2az)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Alexandra+Park+School+N11+2AZ" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="eltham hill school 37.74 ≥13 ≥0 ≥0% greenwich se9 community school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=eltham+hill+school+se9+5ee)" data-state="State" data-borough="Greenwich" data-phase="secondary-only" data-school-type="Community school" data-selectivity="comprehensive/non-selective" data-aps="37.74">
<td data-column="School" data-sort-value="eltham hill school">Eltham Hill School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.74">37.74</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="13.0">≥13</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="greenwich">Greenwich</td>
<td data-column="Postcode district" data-sort-value="se9">SE9</td>
<td data-column="School type" data-sort-value="community school">Community school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=eltham+hill+school+se9+5ee)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Eltham+Hill+School+SE9+5EE" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="wren academy finchley 37.63 60 16 27% barnet n12 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply all-through [map](https://www.google.com/maps/search/?api=1&amp;query=wren+academy+finchley+n12+9hb)" data-state="State" data-borough="Barnet" data-phase="all-through" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.63">
<td data-column="School" data-sort-value="wren academy finchley">Wren Academy Finchley</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.63">37.63</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="60.0">60</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="16.0">16</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="27.0">27%</td>
<td data-column="Area / borough / town" data-sort-value="barnet">Barnet</td>
<td data-column="Postcode district" data-sort-value="n12">N12</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=wren+academy+finchley+n12+9hb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Wren+Academy+Finchley+N12+9HB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="christ&#x27;s church of england comprehensive secondary school 37.61 30 ≥8 ≥27% richmond upon thames tw10 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=christ%27s+church+of+england+comprehensive+secondary+school+tw10+6hw)" data-state="State" data-borough="Richmond upon Thames" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="37.61">
<td data-column="School" data-sort-value="christ&#x27;s church of england comprehensive secondary school">Christ&#x27;s Church of England Comprehensive Secondary School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.61">37.61</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="30.0">30</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="8.0">≥8</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="27.0">≥27%</td>
<td data-column="Area / borough / town" data-sort-value="richmond upon thames">Richmond upon Thames</td>
<td data-column="Postcode district" data-sort-value="tw10">TW10</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=christ%27s+church+of+england+comprehensive+secondary+school+tw10+6hw)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Christ%27s+Church+of+England+Comprehensive+Secondary+School+TW10+6HW" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="sacred heart high school 37.57 22 ≥3 ≥14% hammersmith and fulham w6 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=sacred+heart+high+school+w6+7dg)" data-state="State" data-borough="Hammersmith and Fulham" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.57">
<td data-column="School" data-sort-value="sacred heart high school">Sacred Heart High School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.57">37.57</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="22.0">22</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="3.0">≥3</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="14.0">≥14%</td>
<td data-column="Area / borough / town" data-sort-value="hammersmith and fulham">Hammersmith and Fulham</td>
<td data-column="Postcode district" data-sort-value="w6">W6</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=sacred+heart+high+school+w6+7dg)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Sacred+Heart+High+School+W6+7DG" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st michael&#x27;s catholic college 37.42 32 ≥0 ≥0% southwark se16 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=st+michael%27s+catholic+college+se16+4un)" data-state="State" data-borough="Southwark" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.42">
<td data-column="School" data-sort-value="st michael&#x27;s catholic college">St Michael&#x27;s Catholic College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.42">37.42</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="32.0">32</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="southwark">Southwark</td>
<td data-column="Postcode district" data-sort-value="se16">SE16</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+michael%27s+catholic+college+se16+4un)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Michael%27s+Catholic+College+SE16+4UN" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="wimbledon college 37.39 33 ≥12 ≥36% merton sw19 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=wimbledon+college+sw19+4ns)" data-state="State" data-borough="Merton" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="37.39">
<td data-column="School" data-sort-value="wimbledon college">Wimbledon College</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.39">37.39</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="33.0">33</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="12.0">≥12</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="36.0">≥36%</td>
<td data-column="Area / borough / town" data-sort-value="merton">Merton</td>
<td data-column="Postcode district" data-sort-value="sw19">SW19</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=wimbledon+college+sw19+4ns)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Wimbledon+College+SW19+4NS" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st angela&#x27;s ursuline school 37.26 37 ≥0 ≥0% newham e7 voluntary aided state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=st+angela%27s+ursuline+school+e7+8hu)" data-state="State" data-borough="Newham" data-phase="secondary-only" data-school-type="Voluntary aided" data-selectivity="comprehensive/non-selective" data-aps="37.26">
<td data-column="School" data-sort-value="st angela&#x27;s ursuline school">St Angela&#x27;s Ursuline School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.26">37.26</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="37.0">37</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="0.0">≥0</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="0.0">≥0%</td>
<td data-column="Area / borough / town" data-sort-value="newham">Newham</td>
<td data-column="Postcode district" data-sort-value="e7">E7</td>
<td data-column="School type" data-sort-value="voluntary aided">Voluntary aided</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+angela%27s+ursuline+school+e7+8hu)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+Angela%27s+Ursuline+School+E7+8HU" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="clapton girls&#x27; academy 37.25 44 ≥13 ≥30% hackney e5 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=clapton+girls%27+academy+e5+0rb)" data-state="State" data-borough="Hackney" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.25">
<td data-column="School" data-sort-value="clapton girls&#x27; academy">Clapton Girls&#x27; Academy</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.25">37.25</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="44.0">44</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="13.0">≥13</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="30.0">≥30%</td>
<td data-column="Area / borough / town" data-sort-value="hackney">Hackney</td>
<td data-column="Postcode district" data-sort-value="e5">E5</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=clapton+girls%27+academy+e5+0rb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Clapton+Girls%27+Academy+E5+0RB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="kew house 37.17 ≥20 ≥3 ≥15% hounslow tw8 independent school private ~£26k academically selective/fee-paying no routine internal re-entry exam; external 16+ applicants may sit exams/interviews yes - internal progression normally depends on gcse/subject thresholds secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=kew+house+tw8+0ex)" data-state="Private" data-borough="Hounslow" data-phase="secondary-only" data-school-type="Independent school" data-selectivity="academically selective/fee-paying" data-aps="37.17">
<td data-column="School" data-sort-value="kew house">Kew House</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.17">37.17</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="20.0">≥20</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="3.0">≥3</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="15.0">≥15%</td>
<td data-column="Area / borough / town" data-sort-value="hounslow">Hounslow</td>
<td data-column="Postcode district" data-sort-value="tw8">TW8</td>
<td data-column="School type" data-sort-value="independent school">Independent school</td>
<td data-column="State/private" data-sort-value="private">Private</td>
<td data-column="Approx annual fees" data-sort-value="~£26k">~£26k</td>
<td data-column="Selectivity" data-sort-value="academically selective/fee-paying">academically selective/fee-paying</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no routine internal re-entry exam; external 16+ applicants may sit exams/interviews">No routine internal re-entry exam; external 16+ applicants may sit exams/interviews</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - internal progression normally depends on gcse/subject thresholds">Yes - internal progression normally depends on GCSE/subject thresholds</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=kew+house+tw8+0ex)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Kew+House+TW8+0EX" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="thomas tallis school 37.10 65 ≥12 ≥18% greenwich se3 community school state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=thomas+tallis+school+se3+9px)" data-state="State" data-borough="Greenwich" data-phase="secondary-only" data-school-type="Community school" data-selectivity="comprehensive/non-selective" data-aps="37.1">
<td data-column="School" data-sort-value="thomas tallis school">Thomas Tallis School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.1">37.10</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="65.0">65</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="12.0">≥12</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="18.0">≥18%</td>
<td data-column="Area / borough / town" data-sort-value="greenwich">Greenwich</td>
<td data-column="Postcode district" data-sort-value="se3">SE3</td>
<td data-column="School type" data-sort-value="community school">Community school</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=thomas+tallis+school+se3+9px)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Thomas+Tallis+School+SE3+9PX" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="dunraven school 37.06 57 ≥9 ≥16% lambeth sw16 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply all-through [map](https://www.google.com/maps/search/?api=1&amp;query=dunraven+school+sw16+2qb)" data-state="State" data-borough="Lambeth" data-phase="all-through" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.06">
<td data-column="School" data-sort-value="dunraven school">Dunraven School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.06">37.06</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="57.0">57</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="9.0">≥9</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="16.0">≥16%</td>
<td data-column="Area / borough / town" data-sort-value="lambeth">Lambeth</td>
<td data-column="Postcode district" data-sort-value="sw16">SW16</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="all-through">all-through</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=dunraven+school+sw16+2qb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Dunraven+School+SW16+2QB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="st george&#x27;s catholic school 37.03 ≥16 ≥5 ≥31% westminster w9 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=st+george%27s+catholic+school+w9+1rb)" data-state="State" data-borough="Westminster" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.03">
<td data-column="School" data-sort-value="st george&#x27;s catholic school">St George&#x27;s Catholic School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.03">37.03</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="16.0">≥16</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="5.0">≥5</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="31.0">≥31%</td>
<td data-column="Area / borough / town" data-sort-value="westminster">Westminster</td>
<td data-column="Postcode district" data-sort-value="w9">W9</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=st+george%27s+catholic+school+w9+1rb)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=St+George%27s+Catholic+School+W9+1RB" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
<tr data-search="chiswick school 37.01 44 ≥7 ≥16% hounslow w4 academy state n/a comprehensive/non-selective no extra academic exam noted yes - sixth-form subject/gcse thresholds normally apply secondary-only [map](https://www.google.com/maps/search/?api=1&amp;query=chiswick+school+w4+3un)" data-state="State" data-borough="Hounslow" data-phase="secondary-only" data-school-type="Academy" data-selectivity="comprehensive/non-selective" data-aps="37.01">
<td data-column="School" data-sort-value="chiswick school">Chiswick School</td>
<td class="numeric" data-column="APS per A level entry" data-sort-value="37.01">37.01</td>
<td class="numeric" data-column="Oxbridge applications (2022-2024)" data-sort-value="44.0">44</td>
<td class="numeric" data-column="Oxbridge offers (2022-2024)" data-sort-value="7.0">≥7</td>
<td class="numeric" data-column="Oxbridge offer rate" data-sort-value="16.0">≥16%</td>
<td data-column="Area / borough / town" data-sort-value="hounslow">Hounslow</td>
<td data-column="Postcode district" data-sort-value="w4">W4</td>
<td data-column="School type" data-sort-value="academy">Academy</td>
<td data-column="State/private" data-sort-value="state">State</td>
<td data-column="Approx annual fees" data-sort-value="n/a">N/A</td>
<td data-column="Selectivity" data-sort-value="comprehensive/non-selective">comprehensive/non-selective</td>
<td data-column="Further exam/selection after joining?" data-sort-value="no extra academic exam noted">No extra academic exam noted</td>
<td data-column="GCSE cut-off for sixth form?" data-sort-value="yes - sixth-form subject/gcse thresholds normally apply">Yes - sixth-form subject/GCSE thresholds normally apply</td>
<td data-column="Phase" data-sort-value="secondary-only">secondary-only</td>
<td data-column="Google Maps" data-sort-value="[map](https://www.google.com/maps/search/?api=1&amp;query=chiswick+school+w4+3un)"><a href="https://www.google.com/maps/search/?api=1&amp;amp;query=Chiswick+School+W4+3UN" target="_blank" rel="noopener noreferrer">Map</a></td>
</tr>
</tbody>
    </table>
  </div>
</div>

<section class="secondary-notes">
  <p><strong>Notes:</strong> Private-school fees are approximate annual senior/sixth-form fees, rounded from current published fee schedules where known; for schools marked with a fee range/check note, verify the school fee sheet before making decisions. The Oxbridge columns combine Oxford 2022-2024 aggregate UCAS Apply Centre data with Cambridge 2022, 2023 and 2024 Apply Centre PDFs. Values prefixed with <code>≥</code> are lower bounds where at least one Oxford/Cambridge component was privacy-suppressed in the source PDF (<code>&lt;3</code> or blank). The new sixth-form hurdle columns distinguish a separate exam/selection event from GCSE grade thresholds. “No extra academic exam noted” does not mean automatic A-level entry: GCSE grades, subject-specific thresholds, conduct/attendance, option-block availability and school sixth-form capacity can still apply. Independent schools often test external 16+ applicants even where existing pupils progress by internal GCSE/course thresholds.</p>
</section>

<script id="secondary-school-data" type="application/json">
{&quot;headers&quot;: [&quot;School&quot;, &quot;APS per A level entry&quot;, &quot;Oxbridge applications (2022-2024)&quot;, &quot;Oxbridge offers (2022-2024)&quot;, &quot;Oxbridge offer rate&quot;, &quot;Area / borough / town&quot;, &quot;Postcode district&quot;, &quot;School type&quot;, &quot;State/private&quot;, &quot;Approx annual fees&quot;, &quot;Selectivity&quot;, &quot;Further exam/selection after joining?&quot;, &quot;GCSE cut-off for sixth form?&quot;, &quot;Phase&quot;, &quot;Google Maps&quot;], &quot;rows&quot;: [{&quot;School&quot;: &quot;King&#x27;s College London Maths School&quot;, &quot;APS per A level entry&quot;: &quot;56.11&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;195&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;91&quot;, &quot;Oxbridge offer rate&quot;: &quot;47%&quot;, &quot;Area / borough / town&quot;: &quot;Lambeth&quot;, &quot;Postcode district&quot;: &quot;SE11&quot;, &quot;School type&quot;: &quot;Free school 16-19&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;specialist maths selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;N/A after joining; entry is at 16+ via specialist maths selection&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - 16+ entry uses high GCSE/predicted-grade thresholds&quot;, &quot;Phase&quot;: &quot;sixth-form-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=King%27s+College+London+Maths+School+SE11+6NJ)&quot;}, {&quot;School&quot;: &quot;St Paul&#x27;s Girls&#x27; School&quot;, &quot;APS per A level entry&quot;: &quot;54.75&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;264&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;140&quot;, &quot;Oxbridge offer rate&quot;: &quot;53%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;W6&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£34k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Paul%27s+Girls%27+School+W6+7BS)&quot;}, {&quot;School&quot;: &quot;St Paul&#x27;s School&quot;, &quot;APS per A level entry&quot;: &quot;54.33&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;433&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;141&quot;, &quot;Oxbridge offer rate&quot;: &quot;33%&quot;, &quot;Area / borough / town&quot;: &quot;Richmond upon Thames&quot;, &quot;Postcode district&quot;: &quot;SW13&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£34k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Paul%27s+School+SW13+9JT)&quot;}, {&quot;School&quot;: &quot;Westminster School&quot;, &quot;APS per A level entry&quot;: &quot;53.91&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;537&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;246&quot;, &quot;Oxbridge offer rate&quot;: &quot;46%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;SW1P&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£43k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Westminster+School+SW1P+3PF)&quot;}, {&quot;School&quot;: &quot;King&#x27;s College School&quot;, &quot;APS per A level entry&quot;: &quot;53.09&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;417&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;124&quot;, &quot;Oxbridge offer rate&quot;: &quot;30%&quot;, &quot;Area / borough / town&quot;: &quot;Merton&quot;, &quot;Postcode district&quot;: &quot;SW19&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£31k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=King%27s+College+School+SW19+4TT)&quot;}, {&quot;School&quot;: &quot;Wimbledon High School GDST&quot;, &quot;APS per A level entry&quot;: &quot;52.24&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;117&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥21&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥18%&quot;, &quot;Area / borough / town&quot;: &quot;Merton&quot;, &quot;Postcode district&quot;: &quot;SW19&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Wimbledon+High+School+GDST+SW19+4AB)&quot;}, {&quot;School&quot;: &quot;City of London School for Girls&quot;, &quot;APS per A level entry&quot;: &quot;52.21&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;180&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;49&quot;, &quot;Oxbridge offer rate&quot;: &quot;27%&quot;, &quot;Area / borough / town&quot;: &quot;City of London&quot;, &quot;Postcode district&quot;: &quot;EC2Y&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£31k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=City+of+London+School+for+Girls+EC2Y+8BB)&quot;}, {&quot;School&quot;: &quot;The Godolphin and Latymer School&quot;, &quot;APS per A level entry&quot;: &quot;51.90&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;145&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;29&quot;, &quot;Oxbridge offer rate&quot;: &quot;20%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;W6&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£32k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Godolphin+and+Latymer+School+W6+0PG)&quot;}, {&quot;School&quot;: &quot;The Henrietta Barnett School&quot;, &quot;APS per A level entry&quot;: &quot;51.67&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;228&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;94&quot;, &quot;Oxbridge offer rate&quot;: &quot;41%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;NW11&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective grammar&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No new entrance exam for existing pupils&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Henrietta+Barnett+School+NW11+7BN)&quot;}, {&quot;School&quot;: &quot;City of London School&quot;, &quot;APS per A level entry&quot;: &quot;51.40&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;263&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;84&quot;, &quot;Oxbridge offer rate&quot;: &quot;32%&quot;, &quot;Area / borough / town&quot;: &quot;City of London&quot;, &quot;Postcode district&quot;: &quot;EC4V&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£32k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=City+of+London+School+EC4V+3AL)&quot;}, {&quot;School&quot;: &quot;Alleyn&#x27;s School&quot;, &quot;APS per A level entry&quot;: &quot;51.33&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;182&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;59&quot;, &quot;Oxbridge offer rate&quot;: &quot;32%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE22&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Alleyn%27s+School+SE22+8SU)&quot;}, {&quot;School&quot;: &quot;Highgate School&quot;, &quot;APS per A level entry&quot;: &quot;51.31&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;264&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;87&quot;, &quot;Oxbridge offer rate&quot;: &quot;33%&quot;, &quot;Area / borough / town&quot;: &quot;Haringey&quot;, &quot;Postcode district&quot;: &quot;N6&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£30k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Highgate+School+N6+4AY)&quot;}, {&quot;School&quot;: &quot;Latymer Upper School and Latymer Prep&quot;, &quot;APS per A level entry&quot;: &quot;51.30&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;261&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;75&quot;, &quot;Oxbridge offer rate&quot;: &quot;29%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;W6&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£30k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Latymer+Upper+School+and+Latymer+Prep+W6+9LR)&quot;}, {&quot;School&quot;: &quot;Putney High School&quot;, &quot;APS per A level entry&quot;: &quot;50.55&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;108&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;34&quot;, &quot;Oxbridge offer rate&quot;: &quot;31%&quot;, &quot;Area / borough / town&quot;: &quot;Wandsworth&quot;, &quot;Postcode district&quot;: &quot;SW15&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Putney+High+School+SW15+6BH)&quot;}, {&quot;School&quot;: &quot;South Hampstead High School&quot;, &quot;APS per A level entry&quot;: &quot;50.45&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;122&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;43&quot;, &quot;Oxbridge offer rate&quot;: &quot;35%&quot;, &quot;Area / borough / town&quot;: &quot;Camden&quot;, &quot;Postcode district&quot;: &quot;NW3&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=South+Hampstead+High+School+NW3+5SS)&quot;}, {&quot;School&quot;: &quot;Kingston Grammar School&quot;, &quot;APS per A level entry&quot;: &quot;49.97&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;95&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥19&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥20%&quot;, &quot;Area / borough / town&quot;: &quot;Kingston upon Thames&quot;, &quot;Postcode district&quot;: &quot;KT2&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Kingston+Grammar+School+KT2+6PY)&quot;}, {&quot;School&quot;: &quot;The Tiffin Girls&#x27; School&quot;, &quot;APS per A level entry&quot;: &quot;49.94&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;221&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;65&quot;, &quot;Oxbridge offer rate&quot;: &quot;29%&quot;, &quot;Area / borough / town&quot;: &quot;Kingston upon Thames&quot;, &quot;Postcode district&quot;: &quot;KT2&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective grammar&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No new entrance exam for existing pupils&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Tiffin+Girls%27+School+KT2+5PL)&quot;}, {&quot;School&quot;: &quot;James Allen&#x27;s Girls&#x27; School&quot;, &quot;APS per A level entry&quot;: &quot;49.75&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;130&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;52&quot;, &quot;Oxbridge offer rate&quot;: &quot;40%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE22&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£30k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=James+Allen%27s+Girls%27+School+SE22+8TE)&quot;}, {&quot;School&quot;: &quot;Brampton Manor Academy&quot;, &quot;APS per A level entry&quot;: &quot;49.67&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;872&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;193&quot;, &quot;Oxbridge offer rate&quot;: &quot;22%&quot;, &quot;Area / borough / town&quot;: &quot;Newham&quot;, &quot;Postcode district&quot;: &quot;E6&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive; selective sixth-form entry&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No separate internal exam noted; sixth form is academically selective by grades&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form GCSE/predicted-grade thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Brampton+Manor+Academy+E6+3SQ)&quot;}, {&quot;School&quot;: &quot;London Academy of Excellence&quot;, &quot;APS per A level entry&quot;: &quot;49.49&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;270&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;86&quot;, &quot;Oxbridge offer rate&quot;: &quot;32%&quot;, &quot;Area / borough / town&quot;: &quot;Newham&quot;, &quot;Postcode district&quot;: &quot;E15&quot;, &quot;School type&quot;: &quot;Free school 16-19&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective sixth form&quot;, &quot;Further exam/selection after joining?&quot;: &quot;N/A after joining; entry is at 16+ via selective sixth-form admissions&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - 16+ entry uses GCSE/predicted-grade thresholds&quot;, &quot;Phase&quot;: &quot;sixth-form-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=London+Academy+of+Excellence+E15+1AJ)&quot;}, {&quot;School&quot;: &quot;Tiffin School&quot;, &quot;APS per A level entry&quot;: &quot;49.21&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;403&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;113&quot;, &quot;Oxbridge offer rate&quot;: &quot;28%&quot;, &quot;Area / borough / town&quot;: &quot;Kingston upon Thames&quot;, &quot;Postcode district&quot;: &quot;KT2&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective grammar&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No new entrance exam for existing pupils&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Tiffin+School+KT2+6RL)&quot;}, {&quot;School&quot;: &quot;Michaela Community School&quot;, &quot;APS per A level entry&quot;: &quot;49.17&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;31&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥10&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥32%&quot;, &quot;Area / borough / town&quot;: &quot;Brent&quot;, &quot;Postcode district&quot;: &quot;HA9&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Michaela+Community+School+HA9+0UU)&quot;}, {&quot;School&quot;: &quot;Notting Hill &amp; Ealing High School GDST&quot;, &quot;APS per A level entry&quot;: &quot;49.12&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;69&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥17&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥25%&quot;, &quot;Area / borough / town&quot;: &quot;Ealing&quot;, &quot;Postcode district&quot;: &quot;W13&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Notting+Hill+%26+Ealing+High+School+GDST+W13+8AX)&quot;}, {&quot;School&quot;: &quot;University College School&quot;, &quot;APS per A level entry&quot;: &quot;48.91&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;225&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;51&quot;, &quot;Oxbridge offer rate&quot;: &quot;23%&quot;, &quot;Area / borough / town&quot;: &quot;Camden&quot;, &quot;Postcode district&quot;: &quot;NW3&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=University+College+School+NW3+6XH)&quot;}, {&quot;School&quot;: &quot;Francis Holland School&quot;, &quot;APS per A level entry&quot;: &quot;48.78&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;37&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥7&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥19%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;SW1W&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Francis+Holland+School+SW1W+8JF)&quot;}, {&quot;School&quot;: &quot;Trinity School&quot;, &quot;APS per A level entry&quot;: &quot;48.73&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;148&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;40&quot;, &quot;Oxbridge offer rate&quot;: &quot;27%&quot;, &quot;Area / borough / town&quot;: &quot;Croydon&quot;, &quot;Postcode district&quot;: &quot;CR9&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£25k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Trinity+School+CR9+7AT)&quot;}, {&quot;School&quot;: &quot;Newham Collegiate Sixth Form Centre, City of London Academy&quot;, &quot;APS per A level entry&quot;: &quot;48.68&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;365&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;78&quot;, &quot;Oxbridge offer rate&quot;: &quot;21%&quot;, &quot;Area / borough / town&quot;: &quot;Newham&quot;, &quot;Postcode district&quot;: &quot;E6&quot;, &quot;School type&quot;: &quot;Free school 16-19&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective sixth form&quot;, &quot;Further exam/selection after joining?&quot;: &quot;N/A after joining; entry is at 16+ via selective sixth-form admissions&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - 16+ entry uses GCSE/predicted-grade thresholds&quot;, &quot;Phase&quot;: &quot;sixth-form-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Newham+Collegiate+Sixth+Form+Centre%2C+City+of+London+Academy+E6+2BB)&quot;}, {&quot;School&quot;: &quot;Queen&#x27;s College, London&quot;, &quot;APS per A level entry&quot;: &quot;48.40&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;26&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥19%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;W1G&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Queen%27s+College%2C+London+W1G+8BT)&quot;}, {&quot;School&quot;: &quot;Channing School&quot;, &quot;APS per A level entry&quot;: &quot;48.27&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;44&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥18%&quot;, &quot;Area / borough / town&quot;: &quot;Haringey&quot;, &quot;Postcode district&quot;: &quot;N6&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£28k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Channing+School+N6+5HF)&quot;}, {&quot;School&quot;: &quot;Eltham College&quot;, &quot;APS per A level entry&quot;: &quot;48.21&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;100&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;25&quot;, &quot;Oxbridge offer rate&quot;: &quot;25%&quot;, &quot;Area / borough / town&quot;: &quot;Bromley&quot;, &quot;Postcode district&quot;: &quot;SE9&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Eltham+College+SE9+4QF)&quot;}, {&quot;School&quot;: &quot;Emanuel School&quot;, &quot;APS per A level entry&quot;: &quot;47.94&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;55&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥21&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥38%&quot;, &quot;Area / borough / town&quot;: &quot;Wandsworth&quot;, &quot;Postcode district&quot;: &quot;SW11&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Emanuel+School+SW11+1HS)&quot;}, {&quot;School&quot;: &quot;Dulwich College&quot;, &quot;APS per A level entry&quot;: &quot;47.92&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;274&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;60&quot;, &quot;Oxbridge offer rate&quot;: &quot;22%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE21&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£31k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Dulwich+College+SE21+7LD)&quot;}, {&quot;School&quot;: &quot;The Latymer School&quot;, &quot;APS per A level entry&quot;: &quot;47.28&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;241&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;58&quot;, &quot;Oxbridge offer rate&quot;: &quot;24%&quot;, &quot;Area / borough / town&quot;: &quot;Enfield&quot;, &quot;Postcode district&quot;: &quot;N9&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective grammar&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No new entrance exam for existing pupils&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Latymer+School+N9+9TN)&quot;}, {&quot;School&quot;: &quot;St Augustine&#x27;s Priory&quot;, &quot;APS per A level entry&quot;: &quot;46.97&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Ealing&quot;, &quot;Postcode district&quot;: &quot;W5&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£22k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Augustine%27s+Priory+W5+2JL)&quot;}, {&quot;School&quot;: &quot;Wallington County Grammar School&quot;, &quot;APS per A level entry&quot;: &quot;46.95&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;137&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;28&quot;, &quot;Oxbridge offer rate&quot;: &quot;20%&quot;, &quot;Area / borough / town&quot;: &quot;Sutton&quot;, &quot;Postcode district&quot;: &quot;SM6&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective grammar&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No new entrance exam for existing pupils&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Wallington+County+Grammar+School+SM6+7PH)&quot;}, {&quot;School&quot;: &quot;St Dunstan&#x27;s College&quot;, &quot;APS per A level entry&quot;: &quot;46.90&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;48&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥16&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥33%&quot;, &quot;Area / borough / town&quot;: &quot;Lewisham&quot;, &quot;Postcode district&quot;: &quot;SE6&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£26k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Dunstan%27s+College+SE6+4TY)&quot;}, {&quot;School&quot;: &quot;St Michael&#x27;s Catholic Grammar School&quot;, &quot;APS per A level entry&quot;: &quot;46.84&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;121&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;24&quot;, &quot;Oxbridge offer rate&quot;: &quot;20%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;N12&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective grammar&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No new entrance exam for existing pupils&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Michael%27s+Catholic+Grammar+School+N12+7NJ)&quot;}, {&quot;School&quot;: &quot;Colfe&#x27;s School&quot;, &quot;APS per A level entry&quot;: &quot;46.71&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;63&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥11&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥17%&quot;, &quot;Area / borough / town&quot;: &quot;Greenwich&quot;, &quot;Postcode district&quot;: &quot;SE12&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£26k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Colfe%27s+School+SE12+8AW)&quot;}, {&quot;School&quot;: &quot;Francis Holland School&quot;, &quot;APS per A level entry&quot;: &quot;46.67&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;37&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥7&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥19%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;NW1&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Francis+Holland+School+NW1+6XR)&quot;}, {&quot;School&quot;: &quot;Lycee Francais Charles de Gaulle&quot;, &quot;APS per A level entry&quot;: &quot;46.54&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;163&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥12&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥7%&quot;, &quot;Area / borough / town&quot;: &quot;Kensington and Chelsea&quot;, &quot;Postcode district&quot;: &quot;SW7&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£16k-£22k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Lycee+Francais+Charles+de+Gaulle+SW7+2DG)&quot;}, {&quot;School&quot;: &quot;City of London Academy, Highgate Hill&quot;, &quot;APS per A level entry&quot;: &quot;46.00&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;8&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥62%&quot;, &quot;Area / borough / town&quot;: &quot;Islington&quot;, &quot;Postcode district&quot;: &quot;N19&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=City+of+London+Academy%2C+Highgate+Hill+N19+3EU)&quot;}, {&quot;School&quot;: &quot;Queen&#x27;s Gate School&quot;, &quot;APS per A level entry&quot;: &quot;45.81&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥28&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥29%&quot;, &quot;Area / borough / town&quot;: &quot;Kensington and Chelsea&quot;, &quot;Postcode district&quot;: &quot;SW7&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Queen%27s+Gate+School+SW7+5LE)&quot;}, {&quot;School&quot;: &quot;The Harrodian School&quot;, &quot;APS per A level entry&quot;: &quot;45.79&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;40&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥6&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥15%&quot;, &quot;Area / borough / town&quot;: &quot;Richmond upon Thames&quot;, &quot;Postcode district&quot;: &quot;SW13&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£28k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Harrodian+School+SW13+9QN)&quot;}, {&quot;School&quot;: &quot;JFS&quot;, &quot;APS per A level entry&quot;: &quot;45.76&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;109&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;19&quot;, &quot;Oxbridge offer rate&quot;: &quot;17%&quot;, &quot;Area / borough / town&quot;: &quot;Brent&quot;, &quot;Postcode district&quot;: &quot;HA3&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=JFS+HA3+9TE)&quot;}, {&quot;School&quot;: &quot;London Academy of Excellence Tottenham&quot;, &quot;APS per A level entry&quot;: &quot;45.54&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;200&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥35&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥18%&quot;, &quot;Area / borough / town&quot;: &quot;Haringey&quot;, &quot;Postcode district&quot;: &quot;N17&quot;, &quot;School type&quot;: &quot;Free school 16-19&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective sixth form&quot;, &quot;Further exam/selection after joining?&quot;: &quot;N/A after joining; entry is at 16+ via selective sixth-form admissions&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - 16+ entry uses GCSE/predicted-grade thresholds&quot;, &quot;Phase&quot;: &quot;sixth-form-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=London+Academy+of+Excellence+Tottenham+N17+0BX)&quot;}, {&quot;School&quot;: &quot;The Charter School North Dulwich&quot;, &quot;APS per A level entry&quot;: &quot;45.19&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;100&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;25&quot;, &quot;Oxbridge offer rate&quot;: &quot;25%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE24&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Charter+School+North+Dulwich+SE24+9JH)&quot;}, {&quot;School&quot;: &quot;Ibstock Place School&quot;, &quot;APS per A level entry&quot;: &quot;45.15&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;46&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥20%&quot;, &quot;Area / borough / town&quot;: &quot;Wandsworth&quot;, &quot;Postcode district&quot;: &quot;SW15&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Ibstock+Place+School+SW15+5PY)&quot;}, {&quot;School&quot;: &quot;Forest School&quot;, &quot;APS per A level entry&quot;: &quot;45.00&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;82&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;19&quot;, &quot;Oxbridge offer rate&quot;: &quot;23%&quot;, &quot;Area / borough / town&quot;: &quot;Waltham Forest&quot;, &quot;Postcode district&quot;: &quot;E17&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£25k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Forest+School+E17+3PY)&quot;}, {&quot;School&quot;: &quot;Mill Hill School Foundation&quot;, &quot;APS per A level entry&quot;: &quot;45.00&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;52&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥17%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;NW7&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£32k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Mill+Hill+School+Foundation+NW7+1QS)&quot;}, {&quot;School&quot;: &quot;St Benedict&#x27;s School&quot;, &quot;APS per A level entry&quot;: &quot;44.86&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;48&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥17%&quot;, &quot;Area / borough / town&quot;: &quot;Ealing&quot;, &quot;Postcode district&quot;: &quot;W5&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£24k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Benedict%27s+School+W5+2ES)&quot;}, {&quot;School&quot;: &quot;Brampton College&quot;, &quot;APS per A level entry&quot;: &quot;44.77&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;49&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥10&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥20%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;NW4&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;approx. £20k-£35k; check current fee sheet&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - course/GCSE or equivalent thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Brampton+College+NW4+4DQ)&quot;}, {&quot;School&quot;: &quot;Blackheath High School&quot;, &quot;APS per A level entry&quot;: &quot;44.62&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;17&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥29%&quot;, &quot;Area / borough / town&quot;: &quot;Greenwich&quot;, &quot;Postcode district&quot;: &quot;SE3&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£24k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Blackheath+High+School+SE3+7AG)&quot;}, {&quot;School&quot;: &quot;West London Free School&quot;, &quot;APS per A level entry&quot;: &quot;44.55&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;82&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥23&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥28%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;W6&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=West+London+Free+School+W6+9LP)&quot;}, {&quot;School&quot;: &quot;Harris Westminster Sixth Form&quot;, &quot;APS per A level entry&quot;: &quot;43.98&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;457&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;146&quot;, &quot;Oxbridge offer rate&quot;: &quot;32%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;SW1H&quot;, &quot;School type&quot;: &quot;Free school 16-19&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective sixth form&quot;, &quot;Further exam/selection after joining?&quot;: &quot;N/A after joining; entry is at 16+ via selective sixth-form admissions&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - 16+ entry uses GCSE/predicted-grade thresholds&quot;, &quot;Phase&quot;: &quot;sixth-form-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Harris+Westminster+Sixth+Form+SW1H+9LH)&quot;}, {&quot;School&quot;: &quot;Woodhouse College&quot;, &quot;APS per A level entry&quot;: &quot;43.98&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;405&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;95&quot;, &quot;Oxbridge offer rate&quot;: &quot;23%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;N12&quot;, &quot;School type&quot;: &quot;Sixth form college&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;sixth-form admissions criteria&quot;, &quot;Further exam/selection after joining?&quot;: &quot;N/A after joining; institution starts at sixth form&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - 16+ entry uses GCSE/predicted-grade/course thresholds&quot;, &quot;Phase&quot;: &quot;sixth-form-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Woodhouse+College+N12+9EY)&quot;}, {&quot;School&quot;: &quot;Hasmonean High School for Girls&quot;, &quot;APS per A level entry&quot;: &quot;43.66&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥16&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥31%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;NW7&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;not listed as academically selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Hasmonean+High+School+for+Girls+NW7+2EU)&quot;}, {&quot;School&quot;: &quot;The King Alfred School&quot;, &quot;APS per A level entry&quot;: &quot;43.65&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥13&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;NW11&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£25k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+King+Alfred+School+NW11+7HY)&quot;}, {&quot;School&quot;: &quot;The Camden School for Girls&quot;, &quot;APS per A level entry&quot;: &quot;43.54&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;173&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;68&quot;, &quot;Oxbridge offer rate&quot;: &quot;39%&quot;, &quot;Area / borough / town&quot;: &quot;Camden&quot;, &quot;Postcode district&quot;: &quot;NW5&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Camden+School+for+Girls+NW5+2DB)&quot;}, {&quot;School&quot;: &quot;Twyford Church of England High School&quot;, &quot;APS per A level entry&quot;: &quot;43.51&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;151&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;38&quot;, &quot;Oxbridge offer rate&quot;: &quot;25%&quot;, &quot;Area / borough / town&quot;: &quot;Ealing&quot;, &quot;Postcode district&quot;: &quot;W3&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Twyford+Church+of+England+High+School+W3+9PP)&quot;}, {&quot;School&quot;: &quot;The Totteridge Academy&quot;, &quot;APS per A level entry&quot;: &quot;43.47&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥6&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥83%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;N20&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;not listed as academically selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Totteridge+Academy+N20+8AZ)&quot;}, {&quot;School&quot;: &quot;The London Oratory School&quot;, &quot;APS per A level entry&quot;: &quot;43.27&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;161&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;38&quot;, &quot;Oxbridge offer rate&quot;: &quot;24%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;SW6&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+London+Oratory+School+SW6+1RX)&quot;}, {&quot;School&quot;: &quot;Mossbourne Community Academy&quot;, &quot;APS per A level entry&quot;: &quot;43.22&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;131&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;45&quot;, &quot;Oxbridge offer rate&quot;: &quot;34%&quot;, &quot;Area / borough / town&quot;: &quot;Hackney&quot;, &quot;Postcode district&quot;: &quot;E5&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Mossbourne+Community+Academy+E5+8JY)&quot;}, {&quot;School&quot;: &quot;Menorah High School for Girls&quot;, &quot;APS per A level entry&quot;: &quot;43.13&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;0%&quot;, &quot;Area / borough / town&quot;: &quot;Brent&quot;, &quot;Postcode district&quot;: &quot;NW2&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;not listed as academically selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Menorah+High+School+for+Girls+NW2+7BZ)&quot;}, {&quot;School&quot;: &quot;St James Senior Girls&#x27; School&quot;, &quot;APS per A level entry&quot;: &quot;42.96&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥13&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥4&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥31%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;W14&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+James+Senior+Girls%27+School+W14+8SH)&quot;}, {&quot;School&quot;: &quot;Beth Jacob Grammar School for Girls&quot;, &quot;APS per A level entry&quot;: &quot;42.75&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;0&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;0&quot;, &quot;Oxbridge offer rate&quot;: &quot;0%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;NW4&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;see school&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;11 to 17&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Beth+Jacob+Grammar+School+for+Girls+NW4+2AT)&quot;}, {&quot;School&quot;: &quot;The Cardinal Vaughan Memorial RC School&quot;, &quot;APS per A level entry&quot;: &quot;42.67&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;136&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;37&quot;, &quot;Oxbridge offer rate&quot;: &quot;27%&quot;, &quot;Area / borough / town&quot;: &quot;Kensington and Chelsea&quot;, &quot;Postcode district&quot;: &quot;W14&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Cardinal+Vaughan+Memorial+RC+School+W14+8BZ)&quot;}, {&quot;School&quot;: &quot;Woodford County High School&quot;, &quot;APS per A level entry&quot;: &quot;42.59&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;76&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;25&quot;, &quot;Oxbridge offer rate&quot;: &quot;33%&quot;, &quot;Area / borough / town&quot;: &quot;Waltham Forest&quot;, &quot;Postcode district&quot;: &quot;IG8&quot;, &quot;School type&quot;: &quot;Community school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;selective grammar&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No new entrance exam for existing pupils&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Woodford+County+High+School+IG8+9LA)&quot;}, {&quot;School&quot;: &quot;The St Marylebone CofE School&quot;, &quot;APS per A level entry&quot;: &quot;42.22&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;117&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥24&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥21%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;W1U&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+St+Marylebone+CofE+School+W1U+5BA)&quot;}, {&quot;School&quot;: &quot;Ashcroft Technology Academy&quot;, &quot;APS per A level entry&quot;: &quot;42.03&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;97&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥10&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥10%&quot;, &quot;Area / borough / town&quot;: &quot;Wandsworth&quot;, &quot;Postcode district&quot;: &quot;SW15&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Ashcroft+Technology+Academy+SW15+2UT)&quot;}, {&quot;School&quot;: &quot;Radnor House&quot;, &quot;APS per A level entry&quot;: &quot;41.85&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥11&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Richmond upon Thames&quot;, &quot;Postcode district&quot;: &quot;TW1&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£25k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Radnor+House+TW1+4QG)&quot;}, {&quot;School&quot;: &quot;The St Thomas the Apostle College&quot;, &quot;APS per A level entry&quot;: &quot;41.79&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;54&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥17%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE15&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+St+Thomas+the+Apostle+College+SE15+2EB)&quot;}, {&quot;School&quot;: &quot;Streatham &amp; Clapham High School&quot;, &quot;APS per A level entry&quot;: &quot;41.69&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥19&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥47%&quot;, &quot;Area / borough / town&quot;: &quot;Lambeth&quot;, &quot;Postcode district&quot;: &quot;SW16&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£24k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Streatham+%26+Clapham+High+School+SW16+1AW)&quot;}, {&quot;School&quot;: &quot;Wetherby Senior School&quot;, &quot;APS per A level entry&quot;: &quot;41.50&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;26&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;W1U&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£29k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Wetherby+Senior+School+W1U+2QU)&quot;}, {&quot;School&quot;: &quot;St Catherine&#x27;s School&quot;, &quot;APS per A level entry&quot;: &quot;41.48&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Richmond upon Thames&quot;, &quot;Postcode district&quot;: &quot;TW1&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;approx. £20k-£35k; check current fee sheet&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Catherine%27s+School+TW1+4QJ)&quot;}, {&quot;School&quot;: &quot;Lady Margaret School&quot;, &quot;APS per A level entry&quot;: &quot;41.44&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;42&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥13&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥31%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;SW6&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Lady+Margaret+School+SW6+4UN)&quot;}, {&quot;School&quot;: &quot;Sydenham High School, GDST&quot;, &quot;APS per A level entry&quot;: &quot;41.37&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥17&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Lewisham&quot;, &quot;Postcode district&quot;: &quot;SE26&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£23k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Sydenham+High+School%2C+GDST+SE26+6BL)&quot;}, {&quot;School&quot;: &quot;Paddington Academy&quot;, &quot;APS per A level entry&quot;: &quot;41.32&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;35&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥23%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;W9&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Paddington+Academy+W9+2DR)&quot;}, {&quot;School&quot;: &quot;Holland Park School&quot;, &quot;APS per A level entry&quot;: &quot;41.31&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;58&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥16&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥28%&quot;, &quot;Area / borough / town&quot;: &quot;Kensington and Chelsea&quot;, &quot;Postcode district&quot;: &quot;W8&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;not listed as academically selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Holland+Park+School+W8+7AF)&quot;}, {&quot;School&quot;: &quot;Guildhouse School&quot;, &quot;APS per A level entry&quot;: &quot;40.86&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Camden&quot;, &quot;Postcode district&quot;: &quot;WC1A&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£30k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - course/GCSE or equivalent thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Guildhouse+School+WC1A+2RA)&quot;}, {&quot;School&quot;: &quot;St Mark&#x27;s Church of England Academy&quot;, &quot;APS per A level entry&quot;: &quot;40.44&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Merton&quot;, &quot;Postcode district&quot;: &quot;CR4&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Mark%27s+Church+of+England+Academy+CR4+1SF)&quot;}, {&quot;School&quot;: &quot;Ashbourne College&quot;, &quot;APS per A level entry&quot;: &quot;40.42&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;49&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥18%&quot;, &quot;Area / borough / town&quot;: &quot;Kensington and Chelsea&quot;, &quot;Postcode district&quot;: &quot;W8&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£33k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - course/GCSE or equivalent thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Ashbourne+College+W8+4PL)&quot;}, {&quot;School&quot;: &quot;Lubavitch House School (Senior Girls)&quot;, &quot;APS per A level entry&quot;: &quot;40.30&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;0&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;0&quot;, &quot;Oxbridge offer rate&quot;: &quot;0%&quot;, &quot;Area / borough / town&quot;: &quot;Hackney&quot;, &quot;Postcode district&quot;: &quot;N16&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Lubavitch+House+School+%28Senior+Girls%29+N16+5RP)&quot;}, {&quot;School&quot;: &quot;Mander Portman Woodward School&quot;, &quot;APS per A level entry&quot;: &quot;40.27&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;66&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥12&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥18%&quot;, &quot;Area / borough / town&quot;: &quot;Kensington and Chelsea&quot;, &quot;Postcode district&quot;: &quot;SW7&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£34k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - course/GCSE or equivalent thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Mander+Portman+Woodward+School+SW7+5AB)&quot;}, {&quot;School&quot;: &quot;Old Palace of John Whitgift School&quot;, &quot;APS per A level entry&quot;: &quot;40.23&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;45&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥3&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥7%&quot;, &quot;Area / borough / town&quot;: &quot;Croydon&quot;, &quot;Postcode district&quot;: &quot;CR0&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£22k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;partial all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Old+Palace+of+John+Whitgift+School+CR0+1AX)&quot;}, {&quot;School&quot;: &quot;The Grey Coat Hospital&quot;, &quot;APS per A level entry&quot;: &quot;40.20&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;75&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥23&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥31%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;SW1P&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Grey+Coat+Hospital+SW1P+2DY)&quot;}, {&quot;School&quot;: &quot;Kingsdale Foundation School&quot;, &quot;APS per A level entry&quot;: &quot;40.11&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;62&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;25&quot;, &quot;Oxbridge offer rate&quot;: &quot;40%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE21&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Kingsdale+Foundation+School+SE21+8SQ)&quot;}, {&quot;School&quot;: &quot;The Elms Academy&quot;, &quot;APS per A level entry&quot;: &quot;40.00&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥24&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥33%&quot;, &quot;Area / borough / town&quot;: &quot;Lambeth&quot;, &quot;Postcode district&quot;: &quot;SW4&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Elms+Academy+SW4+9ET)&quot;}, {&quot;School&quot;: &quot;St Mary Magdalene Academy&quot;, &quot;APS per A level entry&quot;: &quot;39.96&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;84&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥17&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥20%&quot;, &quot;Area / borough / town&quot;: &quot;Islington&quot;, &quot;Postcode district&quot;: &quot;N7&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Mary+Magdalene+Academy+N7+8PG)&quot;}, {&quot;School&quot;: &quot;ArtsEd Day School &amp; Sixth Form&quot;, &quot;APS per A level entry&quot;: &quot;39.95&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥3&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Hounslow&quot;, &quot;Postcode district&quot;: &quot;W4&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£25k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - course/GCSE or equivalent thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=ArtsEd+Day+School+%26+Sixth+Form+W4+1LY)&quot;}, {&quot;School&quot;: &quot;Gunnersbury Catholic School&quot;, &quot;APS per A level entry&quot;: &quot;39.92&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;28&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Hounslow&quot;, &quot;Postcode district&quot;: &quot;TW8&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Gunnersbury+Catholic+School+TW8+9LB)&quot;}, {&quot;School&quot;: &quot;Ark Globe Academy&quot;, &quot;APS per A level entry&quot;: &quot;39.51&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;27&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥30%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE1&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Ark+Globe+Academy+SE1+6AG)&quot;}, {&quot;School&quot;: &quot;Hasmonean High School for Boys&quot;, &quot;APS per A level entry&quot;: &quot;39.41&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;23&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥12&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥52%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;NW4&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Hasmonean+High+School+for+Boys+NW4+1NA)&quot;}, {&quot;School&quot;: &quot;City of London Academy, Shoreditch Park&quot;, &quot;APS per A level entry&quot;: &quot;39.34&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥6&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥83%&quot;, &quot;Area / borough / town&quot;: &quot;Hackney&quot;, &quot;Postcode district&quot;: &quot;N1&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;not listed as academically selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=City+of+London+Academy%2C+Shoreditch+Park+N1+5JU)&quot;}, {&quot;School&quot;: &quot;Prendergast School&quot;, &quot;APS per A level entry&quot;: &quot;39.34&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;39&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥23%&quot;, &quot;Area / borough / town&quot;: &quot;Lewisham&quot;, &quot;Postcode district&quot;: &quot;SE4&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Prendergast+School+SE4+1LE)&quot;}, {&quot;School&quot;: &quot;Babington House School&quot;, &quot;APS per A level entry&quot;: &quot;39.33&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Bromley&quot;, &quot;Postcode district&quot;: &quot;BR7&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£22k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Babington+House+School+BR7+5ES)&quot;}, {&quot;School&quot;: &quot;St Gregory&#x27;s Catholic Science College&quot;, &quot;APS per A level entry&quot;: &quot;39.14&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥14&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Brent&quot;, &quot;Postcode district&quot;: &quot;HA3&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Gregory%27s+Catholic+Science+College+HA3+0NB)&quot;}, {&quot;School&quot;: &quot;Bishop Thomas Grant Catholic Secondary School&quot;, &quot;APS per A level entry&quot;: &quot;38.89&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;37&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥22%&quot;, &quot;Area / borough / town&quot;: &quot;Lambeth&quot;, &quot;Postcode district&quot;: &quot;SW16&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Bishop+Thomas+Grant+Catholic+Secondary+School+SW16+2HY)&quot;}, {&quot;School&quot;: &quot;The Fulham Boys School&quot;, &quot;APS per A level entry&quot;: &quot;38.86&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;30&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥11&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥37%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;SW6&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;not listed as academically selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Fulham+Boys+School+SW6+5BD)&quot;}, {&quot;School&quot;: &quot;North Bridge House Senior Canonbury School&quot;, &quot;APS per A level entry&quot;: &quot;38.85&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Islington&quot;, &quot;Postcode district&quot;: &quot;N1&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£27k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=North+Bridge+House+Senior+Canonbury+School+N1+2NQ)&quot;}, {&quot;School&quot;: &quot;Grey Court School&quot;, &quot;APS per A level entry&quot;: &quot;38.84&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;51&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥10%&quot;, &quot;Area / borough / town&quot;: &quot;Richmond upon Thames&quot;, &quot;Postcode district&quot;: &quot;TW10&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Grey+Court+School+TW10+7HN)&quot;}, {&quot;School&quot;: &quot;Ark Bolingbroke Academy&quot;, &quot;APS per A level entry&quot;: &quot;38.82&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;34&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥4&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥12%&quot;, &quot;Area / borough / town&quot;: &quot;Wandsworth&quot;, &quot;Postcode district&quot;: &quot;SW11&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Ark+Bolingbroke+Academy+SW11+6BF)&quot;}, {&quot;School&quot;: &quot;Highlands School&quot;, &quot;APS per A level entry&quot;: &quot;38.82&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥21&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Enfield&quot;, &quot;Postcode district&quot;: &quot;N21&quot;, &quot;School type&quot;: &quot;Community school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Highlands+School+N21+1QQ)&quot;}, {&quot;School&quot;: &quot;Glenthorne High School&quot;, &quot;APS per A level entry&quot;: &quot;38.72&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;46&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥11%&quot;, &quot;Area / borough / town&quot;: &quot;Sutton&quot;, &quot;Postcode district&quot;: &quot;SM3&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;non-selective in selective area&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Glenthorne+High+School+SM3+9PS)&quot;}, {&quot;School&quot;: &quot;The Kingston Academy&quot;, &quot;APS per A level entry&quot;: &quot;38.64&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥27&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥10&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥37%&quot;, &quot;Area / borough / town&quot;: &quot;Kingston upon Thames&quot;, &quot;Postcode district&quot;: &quot;KT2&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=The+Kingston+Academy+KT2+5PE)&quot;}, {&quot;School&quot;: &quot;Central Foundation Boys&#x27; School&quot;, &quot;APS per A level entry&quot;: &quot;38.47&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;29&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥17%&quot;, &quot;Area / borough / town&quot;: &quot;Islington&quot;, &quot;Postcode district&quot;: &quot;EC2A&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Central+Foundation+Boys%27+School+EC2A+4SH)&quot;}, {&quot;School&quot;: &quot;Kensington Aldridge Academy&quot;, &quot;APS per A level entry&quot;: &quot;38.46&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;50&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥4&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥8%&quot;, &quot;Area / borough / town&quot;: &quot;Kensington and Chelsea&quot;, &quot;Postcode district&quot;: &quot;W10&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Kensington+Aldridge+Academy+W10+6EX)&quot;}, {&quot;School&quot;: &quot;Ark Academy&quot;, &quot;APS per A level entry&quot;: &quot;38.39&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;37&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥11&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥30%&quot;, &quot;Area / borough / town&quot;: &quot;Brent&quot;, &quot;Postcode district&quot;: &quot;HA9&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Ark+Academy+HA9+9JR)&quot;}, {&quot;School&quot;: &quot;Parliament Hill School&quot;, &quot;APS per A level entry&quot;: &quot;38.39&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;5&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;0&quot;, &quot;Oxbridge offer rate&quot;: &quot;0%&quot;, &quot;Area / borough / town&quot;: &quot;Camden&quot;, &quot;Postcode district&quot;: &quot;NW5&quot;, &quot;School type&quot;: &quot;Community school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Parliament+Hill+School+NW5+1RL)&quot;}, {&quot;School&quot;: &quot;Orleans Park School&quot;, &quot;APS per A level entry&quot;: &quot;38.29&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;34&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥15%&quot;, &quot;Area / borough / town&quot;: &quot;Richmond upon Thames&quot;, &quot;Postcode district&quot;: &quot;TW1&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Orleans+Park+School+TW1+3BB)&quot;}, {&quot;School&quot;: &quot;Ashmole Academy&quot;, &quot;APS per A level entry&quot;: &quot;38.25&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;85&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥18&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥21%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;N14&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Ashmole+Academy+N14+5RJ)&quot;}, {&quot;School&quot;: &quot;Fine Arts College&quot;, &quot;APS per A level entry&quot;: &quot;38.22&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥10&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Camden&quot;, &quot;Postcode district&quot;: &quot;NW3&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£34k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No internal re-entry exam noted; external 16+ applicants may be assessed/interviewed&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - course/GCSE or equivalent thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Fine+Arts+College+NW3+4YD)&quot;}, {&quot;School&quot;: &quot;Greenshaw High School&quot;, &quot;APS per A level entry&quot;: &quot;38.20&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;36&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥11&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥31%&quot;, &quot;Area / borough / town&quot;: &quot;Sutton&quot;, &quot;Postcode district&quot;: &quot;SM1&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;non-selective in selective area&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Greenshaw+High+School+SM1+3DY)&quot;}, {&quot;School&quot;: &quot;William Perkin Church of England High School&quot;, &quot;APS per A level entry&quot;: &quot;38.13&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥42&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥12%&quot;, &quot;Area / borough / town&quot;: &quot;Ealing&quot;, &quot;Postcode district&quot;: &quot;UB6&quot;, &quot;School type&quot;: &quot;Free school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=William+Perkin+Church+of+England+High+School+UB6+8PR)&quot;}, {&quot;School&quot;: &quot;Alexandra Park School&quot;, &quot;APS per A level entry&quot;: &quot;37.74&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;61&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;18&quot;, &quot;Oxbridge offer rate&quot;: &quot;30%&quot;, &quot;Area / borough / town&quot;: &quot;Haringey&quot;, &quot;Postcode district&quot;: &quot;N11&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Alexandra+Park+School+N11+2AZ)&quot;}, {&quot;School&quot;: &quot;Eltham Hill School&quot;, &quot;APS per A level entry&quot;: &quot;37.74&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥13&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Greenwich&quot;, &quot;Postcode district&quot;: &quot;SE9&quot;, &quot;School type&quot;: &quot;Community school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Eltham+Hill+School+SE9+5EE)&quot;}, {&quot;School&quot;: &quot;Wren Academy Finchley&quot;, &quot;APS per A level entry&quot;: &quot;37.63&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;60&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;16&quot;, &quot;Oxbridge offer rate&quot;: &quot;27%&quot;, &quot;Area / borough / town&quot;: &quot;Barnet&quot;, &quot;Postcode district&quot;: &quot;N12&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Wren+Academy+Finchley+N12+9HB)&quot;}, {&quot;School&quot;: &quot;Christ&#x27;s Church of England Comprehensive Secondary School&quot;, &quot;APS per A level entry&quot;: &quot;37.61&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;30&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥8&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥27%&quot;, &quot;Area / borough / town&quot;: &quot;Richmond upon Thames&quot;, &quot;Postcode district&quot;: &quot;TW10&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Christ%27s+Church+of+England+Comprehensive+Secondary+School+TW10+6HW)&quot;}, {&quot;School&quot;: &quot;Sacred Heart High School&quot;, &quot;APS per A level entry&quot;: &quot;37.57&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;22&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥3&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥14%&quot;, &quot;Area / borough / town&quot;: &quot;Hammersmith and Fulham&quot;, &quot;Postcode district&quot;: &quot;W6&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Sacred+Heart+High+School+W6+7DG)&quot;}, {&quot;School&quot;: &quot;St Michael&#x27;s Catholic College&quot;, &quot;APS per A level entry&quot;: &quot;37.42&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;32&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Southwark&quot;, &quot;Postcode district&quot;: &quot;SE16&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Michael%27s+Catholic+College+SE16+4UN)&quot;}, {&quot;School&quot;: &quot;Wimbledon College&quot;, &quot;APS per A level entry&quot;: &quot;37.39&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;33&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥12&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥36%&quot;, &quot;Area / borough / town&quot;: &quot;Merton&quot;, &quot;Postcode district&quot;: &quot;SW19&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Wimbledon+College+SW19+4NS)&quot;}, {&quot;School&quot;: &quot;St Angela&#x27;s Ursuline School&quot;, &quot;APS per A level entry&quot;: &quot;37.26&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;37&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥0&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥0%&quot;, &quot;Area / borough / town&quot;: &quot;Newham&quot;, &quot;Postcode district&quot;: &quot;E7&quot;, &quot;School type&quot;: &quot;Voluntary aided&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+Angela%27s+Ursuline+School+E7+8HU)&quot;}, {&quot;School&quot;: &quot;Clapton Girls&#x27; Academy&quot;, &quot;APS per A level entry&quot;: &quot;37.25&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;44&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥13&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥30%&quot;, &quot;Area / borough / town&quot;: &quot;Hackney&quot;, &quot;Postcode district&quot;: &quot;E5&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Clapton+Girls%27+Academy+E5+0RB)&quot;}, {&quot;School&quot;: &quot;Kew House&quot;, &quot;APS per A level entry&quot;: &quot;37.17&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥20&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥3&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥15%&quot;, &quot;Area / borough / town&quot;: &quot;Hounslow&quot;, &quot;Postcode district&quot;: &quot;TW8&quot;, &quot;School type&quot;: &quot;Independent school&quot;, &quot;State/private&quot;: &quot;Private&quot;, &quot;Approx annual fees&quot;: &quot;~£26k&quot;, &quot;Selectivity&quot;: &quot;academically selective/fee-paying&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No routine internal re-entry exam; external 16+ applicants may sit exams/interviews&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - internal progression normally depends on GCSE/subject thresholds&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Kew+House+TW8+0EX)&quot;}, {&quot;School&quot;: &quot;Thomas Tallis School&quot;, &quot;APS per A level entry&quot;: &quot;37.10&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;65&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥12&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥18%&quot;, &quot;Area / borough / town&quot;: &quot;Greenwich&quot;, &quot;Postcode district&quot;: &quot;SE3&quot;, &quot;School type&quot;: &quot;Community school&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Thomas+Tallis+School+SE3+9PX)&quot;}, {&quot;School&quot;: &quot;Dunraven School&quot;, &quot;APS per A level entry&quot;: &quot;37.06&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;57&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥9&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥16%&quot;, &quot;Area / borough / town&quot;: &quot;Lambeth&quot;, &quot;Postcode district&quot;: &quot;SW16&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;all-through&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Dunraven+School+SW16+2QB)&quot;}, {&quot;School&quot;: &quot;St George&#x27;s Catholic School&quot;, &quot;APS per A level entry&quot;: &quot;37.03&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;≥16&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥5&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥31%&quot;, &quot;Area / borough / town&quot;: &quot;Westminster&quot;, &quot;Postcode district&quot;: &quot;W9&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=St+George%27s+Catholic+School+W9+1RB)&quot;}, {&quot;School&quot;: &quot;Chiswick School&quot;, &quot;APS per A level entry&quot;: &quot;37.01&quot;, &quot;Oxbridge applications (2022-2024)&quot;: &quot;44&quot;, &quot;Oxbridge offers (2022-2024)&quot;: &quot;≥7&quot;, &quot;Oxbridge offer rate&quot;: &quot;≥16%&quot;, &quot;Area / borough / town&quot;: &quot;Hounslow&quot;, &quot;Postcode district&quot;: &quot;W4&quot;, &quot;School type&quot;: &quot;Academy&quot;, &quot;State/private&quot;: &quot;State&quot;, &quot;Approx annual fees&quot;: &quot;N/A&quot;, &quot;Selectivity&quot;: &quot;comprehensive/non-selective&quot;, &quot;Further exam/selection after joining?&quot;: &quot;No extra academic exam noted&quot;, &quot;GCSE cut-off for sixth form?&quot;: &quot;Yes - sixth-form subject/GCSE thresholds normally apply&quot;, &quot;Phase&quot;: &quot;secondary-only&quot;, &quot;Google Maps&quot;: &quot;[Map](https://www.google.com/maps/search/?api=1&amp;query=Chiswick+School+W4+3UN)&quot;}], &quot;notes&quot;: &quot;Private-school fees are approximate annual senior/sixth-form fees, rounded from current published fee schedules where known; for schools marked with a fee range/check note, verify the school fee sheet before making decisions. The Oxbridge columns combine Oxford 2022-2024 aggregate UCAS Apply Centre data with Cambridge 2022, 2023 and 2024 Apply Centre PDFs. Values prefixed with `≥` are lower bounds where at least one Oxford/Cambridge component was privacy-suppressed in the source PDF (`&lt;3` or blank). The new sixth-form hurdle columns distinguish a separate exam/selection event from GCSE grade thresholds. “No extra academic exam noted” does not mean automatic A-level entry: GCSE grades, subject-specific thresholds, conduct/attendance, option-block availability and school sixth-form capacity can still apply. Independent schools often test external 16+ applicants even where existing pupils progress by internal GCSE/course thresholds.&quot;}
</script>

<script>
(function () {
  const table = document.getElementById("secondarySchoolsTable");
  if (!table) return;
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.rows);
  const filters = {
    search: document.getElementById("secondarySearch"),
    state: document.getElementById("secondaryStateFilter"),
    borough: document.getElementById("secondaryBoroughFilter"),
    phase: document.getElementById("secondaryPhaseFilter"),
    type: document.getElementById("secondaryTypeFilter"),
    selectivity: document.getElementById("secondarySelectivityFilter"),
    minAps: document.getElementById("secondaryMinAps"),
    limit: document.getElementById("secondaryRowLimit")
  };
  const summary = document.getElementById("secondaryFilterSummary");
  let currentSort = { column: "APS per A level entry", direction: "desc", type: "number" };

  function sortRows() {
    rows.sort((a, b) => {
      const aCell = a.querySelector(`[data-column="${currentSort.column}"]`);
      const bCell = b.querySelector(`[data-column="${currentSort.column}"]`);
      const aRaw = aCell ? aCell.dataset.sortValue : "";
      const bRaw = bCell ? bCell.dataset.sortValue : "";
      let comparison;
      if (currentSort.type === "number") {
        const aValue = Number(aRaw);
        const bValue = Number(bRaw);
        comparison = (Number.isFinite(aValue) ? aValue : -Infinity) - (Number.isFinite(bValue) ? bValue : -Infinity);
      } else {
        comparison = aRaw.localeCompare(bRaw);
      }
      return currentSort.direction === "asc" ? comparison : -comparison;
    });
  }

  function rowMatches(row) {
    const query = filters.search.value.trim().toLowerCase();
    const minAps = Number(filters.minAps.value);
    return (!query || row.dataset.search.includes(query)) &&
      (!filters.state.value || row.dataset.state === filters.state.value) &&
      (!filters.borough.value || row.dataset.borough === filters.borough.value) &&
      (!filters.phase.value || row.dataset.phase === filters.phase.value) &&
      (!filters.type.value || row.dataset.schoolType === filters.type.value) &&
      (!filters.selectivity.value || row.dataset.selectivity === filters.selectivity.value) &&
      (!Number.isFinite(minAps) || Number(row.dataset.aps) >= minAps);
  }

  function applyFilters() {
    sortRows();
    const limit = Number(filters.limit.value);
    let shown = 0;
    rows.forEach((row) => {
      const visible = rowMatches(row) && (!Number.isFinite(limit) || !limit || shown < limit);
      row.hidden = !visible;
      if (visible) shown += 1;
    });
    rows.forEach((row) => tbody.appendChild(row));
    summary.textContent = `${shown} of ${rows.length} schools shown. Click any column header to sort.`;
  }

  table.querySelectorAll(".sort-button").forEach((button) => {
    button.addEventListener("click", () => {
      const column = button.dataset.column;
      const type = button.dataset.sortType;
      const sameColumn = currentSort.column === column;
      currentSort = {
        column,
        type,
        direction: sameColumn && currentSort.direction === "desc" ? "asc" : "desc"
      };
      applyFilters();
    });
  });

  Object.values(filters).forEach((control) => {
    control.addEventListener("input", applyFilters);
    control.addEventListener("change", applyFilters);
  });

  applyFilters();
}());
</script>
