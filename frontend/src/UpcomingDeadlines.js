import React from "react";
import MaterialTable from "material-table";

class UpcomingDeadlines extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          columns: [
              { title: 'Due Date',
                field: 'datetime',
                type: 'date',
                render: rowData => <span>{this.displayDate(rowData['datetime'])}</span>,},
              { title: 'Deadline',
                field: 'deadline-name', },


              { title: 'Defendant',
                field: 'defendant' },
              { title: 'CR#',
                field: 'case-number',},
              { title: 'Judge',
                field: 'judge' ,},
              { title: 'Defense',
                field: 'defense-attorney' },

              // This column is only for storing the pk - user should not see
              { title: 'PK - YOU SHOULDN\'T SEE ME',
                field: 'pk',
                hidden: true },
          ],
          tableData: [],
          jsonData: []
      }
  }

  displayDate(date) { // TODO Move this function to App.js or utils
    /* Displays a date as M/D/YYYY.
    * param date: either Date or string
    * */

    let realDate = new Date();
    if (date) {
      if (typeof(date) === 'string') {
        realDate = new Date(date);
      } else {
        realDate = date;
      }

      // Could use Moment.js here instead...
      const day = realDate.getDate().toString();
      const month = (realDate.getMonth() + 1).toString();
      const year = realDate.getFullYear().toString();

      const dateString = month.concat('/', day, '/', year)

      return dateString;
    } else {
      return '';
    }
  }

  componentDidMount() {
    this.fetchDeadlines();
  }

  fetchDeadlines() {
      return fetch("/api/deadlines")
          .then(response => response.json())
          .then(deadlines => this.populateTable(deadlines))
  }

  populateTable(deadlines) {

      // Save JSON Data to state
      this.setState({jsonData: deadlines});

      // Populate table with data
      let dataArray = [];
      deadlines.forEach(function (deadlineJSON) {
          let row = {};

          row['deadline-name'] = deadlineJSON['deadline_name'];
          row['datetime'] = deadlineJSON['datetime'];
          row['defendant'] = deadlineJSON['defendant'];
          row['case-number'] = deadlineJSON['case_number'];
          row['judge'] = deadlineJSON['judge'];
          row['defense-attorney'] = deadlineJSON['defense_attorney'];
          row['pk'] = deadlineJSON['id'];

          dataArray.push(row);

      });

      this.setState(
          {tableData: dataArray}
      )
  }

  render() {
    return (
        <MaterialTable
            title="Upcoming Deadlines"
            columns={this.state.columns}
            data={this.state.tableData}
            options={{
                pageSize: 10
            }}
            actions={[
                {
                    icon: 'check',
                    tooltip: 'Complete Deadline',
                    onClick: (event, rowData) => {
                        let pk = rowData['pk'];
                        window.location.href = `complete/${pk}`;
                    }
                }
            ]}
            />
    );
  }

}

export default UpcomingDeadlines;
