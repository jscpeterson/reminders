import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import MaterialTable from 'material-table'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      columns: [
        { title: 'Defendant', field: 'defendant', editable: 'never' },
        { title: 'CR#', field: 'case_number', editable: 'never' },
        { title: 'Judge', field: 'judge' , editable: 'onUpdate'},
        { title: 'Defense', field: 'defense_attorney' , editable: 'onUpdate' },

        { title: 'Notes', field: 'notes', editable: 'onUpdate' },

        { title: 'Witness List', field: 'witness_list', type:'date', editable: 'never' },
        { title: 'Scheduling Conference', field: 'scheduling_conf', type: 'date', editable: 'never' },
        { title: 'Request PTIs', field: '3', type: 'request_pti', editable: 'never' },
        { title: 'Conduct PTIs', field: '4', type: 'conduct_pti', editable: 'never' },
        { title: 'Witness PTIs', field: '5', type: 'witness_pti', editable: 'never' },
        { title: 'Scientific Evidence', field: 'scientific_evidence', type: 'date', editable: 'never' },
        { title: 'Pretrial Motion Filing', field: 'pretrial_motion_filing', type: 'date', editable: 'never' },
        { title: 'Pretrial Conference', field: 'pretrial_conf', type: 'date', editable: 'never' },
        { title: 'Final Witness List', field: 'final_witness_list', type: 'date', editable: 'never' },
        { title: 'Need for Interpreter', field: 'need_for_interpreter', type: 'date', editable: 'never' },
        { title: 'Plea Agreement', field: 'plea_agreement', type: 'date', editable: 'never' },
        { title: 'Trial', field: '11', type: 'trial', editable: 'never' },

      ],
      data: []
    }
  }

    // witness_list
    // scheduling_conf
    // request_pti
    // conduct_pti
    // witness_pti
    // scientific_evidence
    // pretrial_motion_filing
    // pretrial_conf
    // final_witness_list
    // need_for_interpreter
    // plea_agreement
    // trial

  populateJson(cases) {
    // let dataArray = [
    //     { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
    //       1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
    //   },
    //
    //   { defendant: 'Mitch Connor', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
    //       1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
    //   },
    //
    //   { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Joe Brown', defense: 'Lionel Hutz',
    //       1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
    //   },
    //
    //   { defendant: 'Billy the Kid', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
    //       1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
    //   },
    //
    //   { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
    //       1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
    //   },
    //   {
    //     defendant: 'Hulk Hogan', case_number: '2019-00001', judge: 'Maury', defense: 'Saul Goodman',
    //     1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
    //   }
    //  ]

    let dataArray = [];

    cases.forEach(function(casejson){
        let row = {};

        // Populate basic data
        row['defendant'] = casejson['defendant'];
        row['case_number'] = casejson['case_number'];
        row['judge'] = casejson['judge'];
        row['defense_attorney'] = casejson['defense_attorney'];
        row['notes'] = casejson['notes'];

        // Set up call for deadlines
        let url =`http://127.0.0.1:8000/api/deadlines?case=${casejson['case_number']}`;
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
    return fetch("http://127.0.0.1:8000/api/cases/")
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
            pageSize: 14
        }}
          // TODO Remove trash can icon
          // TODO Remove ability to add rows
          // TODO Make notes field bigger
        editable={{
            isDeletable: rowData => null, // no rows should be deletable
          onRowAdd: newData =>
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
              // TODO Updating the row should PATCH to case data
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
