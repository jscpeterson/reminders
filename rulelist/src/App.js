import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import MaterialTable from 'material-table'
import Cookies from 'js-cookie'

class App extends React.Component {
  constructor(props) {
    super(props);

    // EDITABLE FIELDS TODO move to constants.js later
      // Judge
      // Defense
      // Notes

    this.state = {
      columns: [
        { title: 'Defendant',
            field: 'defendant',
            editable: 'never' },
        { title: 'CR#',
            field: 'case_number',
            editable: 'never' },
        { title: 'Judge',
            field: 'judge' ,
            editable: 'onUpdate'},
        { title: 'Defense',
            field: 'defense_attorney' ,
            editable: 'onUpdate' },

          // TODO Notes cell should be larger
        { title: 'Notes', field: 'notes', editable: 'onUpdate' },

          // TODO Deadline cell data isn't visible until a column is selected
        { title: 'Witness List',
            field: 'witness_list',
            type:'date',
            editable: 'never' },
        { title: 'Scheduling Conference',
            field: 'scheduling_conf',
            type: 'date',
            editable: 'never' },
        { title: 'Request PTIs',
            field: 'request_pti',
            type: 'date',
            editable: 'never' },
        { title: 'Conduct PTIs',
            field: 'conduct_pti',
            type: 'date',
            editable: 'never' },
        { title: 'Witness PTIs',
            field: 'witness_pti',
            type: 'date',
            editable: 'never' },
        { title: 'Scientific Evidence',
            field: 'scientific_evidence',
            type: 'date',
            editable: 'never' },
        { title: 'Pretrial Motion Filing',
            field: 'pretrial_motion_filing',
            type: 'date',
            editable: 'never' },
        { title: 'Pretrial Conference',
            field: 'pretrial_conf',
            type: 'date',
            editable: 'never' },
        { title: 'Final Witness List',
            field: 'final_witness_list',
            type: 'date',
            editable: 'never' },
        { title: 'Need for Interpreter',
            field: 'need_for_interpreter',
            type: 'date',
            editable: 'never' },
        { title: 'Plea Agreement',
            field: 'plea_agreement',
            type: 'date',
            editable: 'never' },
        { title: 'Trial',
            field: 'trial',
            type: 'date',
            editable: 'never' },
      ],

      tableData: [],

      jsonData: []

    }
  }

  populateJson(cases) {

    // Save JSON Data
    this.setState({jsonData : cases});

    let dataArray = [];

    cases.forEach(function(casejson){
        let row = {};

        // Populate basic data for table
        row['defendant'] = casejson['defendant'];
        row['case_number'] = casejson['case_number'];
        row['judge'] = casejson['judge'];
        row['defense_attorney'] = casejson['defense_attorney'];
        row['notes'] = casejson['notes'];

        const deadlines = casejson['deadline_set']
        
        deadlines.forEach(function(deadline){
                const type = deadline['type'];
                let key = '';
                switch (type) { // TODO move to constants.js later
                    case 1:
                        key = 'scheduling_conf';
                        break;
                    case 2:
                        key = 'witness_list';
                        break;
                    case 3:
                        key = 'request_pti';
                        break;
                    case 4:
                        key = 'conduct_pti';
                        break;
                    case 5:
                        key = 'witness_pti';
                        break;
                    case 6:
                        key = 'scientific_evidence';
                        break;
                    case 7:
                        key = 'pretrial_motion_filing';
                        break;
                    case 10:
                        key = 'pretrial_conf';
                        break;
                    case 11:
                        key = 'final_witness_list';
                        break;
                    case 12:
                        key = 'need_for_interpreter';
                        break;
                    case 13:
                        key = 'plea_agreement';
                        break;
                    case 14:
                        key = 'trial';
                        break;
                }
                row[key] = deadline['datetime'].slice(0, 10); // FIXME Table needs to be tweaked to view date
            });

        dataArray.push(row);
    });

    this.setState(
        {tableData: dataArray}
    )
  }

  fetchJson() {
    return fetch("/api/cases/")
          .then(response => response.json())
          .then(cases => this.populateJson(cases))
  }

  updateData(data) {
      let pk = data['id'];
      let url = `/api/cases/${pk}/`;
      return fetch(url, {
          method: 'PUT',
          body: JSON.stringify(data),
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': Cookies.get('csrftoken')
          }
    })
  }

  componentDidMount() {
    this.fetchJson();
  }

  render() {
    return (
      <MaterialTable
        title="Rule List"
        columns={this.state.columns}
        data={this.state.tableData}
        options={{
            pageSize: 10
        }}
        editable={{
            isDeletable: rowData => null, // TODO this prevents rows from being deleted but trash can icon is still there
          onRowAdd: newData =>
            // TODO User should not be able to add rows
            new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  const data = this.state.tableData;
                  data.push(newData);
                  this.setState({ data }, () => resolve());
                }
                resolve()
              }, 1000)
            }),
          onRowUpdate: (newData, oldData) =>
              new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  // standard row update behavior
                  const data = this.state.tableData;
                  const index = data.indexOf(oldData);
                  data[index] = newData;

                  // update json data from newData
                  let json = this.state.jsonData[index];
                  // EDITABLE FIELDS TODO move to constants.js later
                    // Judge
                    // Defense
                    // Notes
                  json['judge'] = newData['judge'];
                  json['defense_attorney'] = newData['defense_attorney'];
                  json['notes'] = newData['notes'];
                  this.updateData(json);

                  // final part of standard row update behavior
                  this.setState({ data }, () => resolve());
                }
                resolve()
              }, 1000)
            }),
          onRowDelete: oldData =>
            // TODO User should not be able to delete rows
            new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  let data = this.state.tableData;
                  const index = data.indexOf(oldData);
                  data.splice(index, 1);
                  this.setState({ data }, () => resolve());
                }
                resolve()
              }, 1000)
            }),
        }}
      />
    )
  }
}

export default App;
