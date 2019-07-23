import * as React from "react";
import MaterialTable from "material-table";

class ManagementTable extends React.Component {
  constructor(props) {
      super(props);

      this.state = {
          columns: [
              {
                  title: 'Defendant',
                  field: 'defendant'
              },
              {
                  title: 'CR#',
                  field: 'case-number',
              },
              {
                  title: 'Judge',
                  field: 'judge' ,
              },
              {
                  title: 'Defense',
                  field: 'defense-attorney' ,
              },
              {
                  title: 'Attorney',
                  field: 'prosecutor' ,
              },
              {
                  title: 'Secretary',
                  field: 'secretary' ,
              },
          ],
          tableData: [],
      }
  }

  componentDidMount() {
      this.fetchCases();
  }

  fetchCases() {
      return fetch("/api/cases/")
          .then(response => response.json())
          .then(cases => this.populateTable(cases))
  }

  populateTable(cases) {

      let dataArray = [];

      cases.forEach(function(caseJSON) {
          let row = {};

          row['defendant'] = caseJSON['defendant'];
          row['case-number'] = caseJSON['case_number'];
          row['judge'] = caseJSON['judge'];
          row['defense-attorney'] = caseJSON['defense_attorney'];
          row['prosecutor'] = caseJSON['prosecutor_name'];
          row['secretary'] = caseJSON['secretary_name'];

          dataArray.push(row);
      });

      this.setState(
          {tableData: dataArray}
      )
  }

  render() {
      return (

          <MaterialTable
              title="Cases You Are Managing"
              columns={this.state.columns}
              data={this.state.tableData}
              options={{
                  selection: true
              }}
              actions={[
                  {
                      tooltip: 'Reassign Selected Cases',
                      icon: 'assignment_ind',
                      onClick: (event, data) => console.log(data)
                  },
              ]}
          />
      )
  }
}

export default ManagementTable;