import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import MaterialTable from 'material-table'

class App extends React.Component {
  constructor(props) {
    super(props);
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

      data: []

    }
  }

  populateJson(cases) {

    let dataArray = [];

    cases.forEach(function(casejson){
        let row = {};

        // Populate basic data
        row['defendant'] = casejson['defendant'];
        row['case_number'] = casejson['case_number'];
        row['judge'] = casejson['judge'];
        row['defense_attorney'] = casejson['defense_attorney'];
        row['notes'] = casejson['notes'];

        // Send request to api for case deadlines
        let url =`/api/deadlines?case=${casejson['case_number']}`; // TODO This is only the dev URL
        console.log(url);
        fetch(url)
            .then(response => response.json())
            .then(deadlines => {
                deadlines.forEach(function(deadline){
                    const type = deadline['type'];
                    let key = '';
                    switch (type) {
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
            });

        dataArray.push(row);
    });

    this.setState(
        {data: dataArray}
    )
  }

  fetchJson() {
    return fetch("/api/cases/") // TODO This is only the dev URL
          .then(response => response.json())
          .then(cases => this.populateJson(cases))
  }

  componentDidMount() {
    this.fetchJson();
  }

  render() {
    return (
      <MaterialTable
        title="Rule List"
        columns={this.state.columns}
        data={this.state.data}
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
                  const data = this.state.data;
                  data.push(newData);
                  this.setState({ data }, () => resolve());
                }
                resolve()
              }, 1000)
            }),
          onRowUpdate: (newData, oldData) =>
              // TODO Updating the row should POST/PUT/PATCH to case data
              new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  const data = this.state.data;
                  const index = data.indexOf(oldData);
                  data[index] = newData;
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
                  let data = this.state.data;
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
