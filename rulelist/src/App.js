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

        { title: 'Witness List', field: 'witness_list', type: 'date', editable: 'never' },
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

  populateJson(jsonArray) {
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

    let dataArray = []

    jsonArray.forEach(function(json){
        let row = {};
        row['defendant'] = json['defendant'];
        row['case_number'] = json['case_number'];
        row['judge'] = json['judge']; // TODO Need to get correct judge
        row['defense_attorney'] = json['defense_attorney'];
        row['notes'] = json['notes'];
        dataArray.push(row);
    });

    this.setState(
        {data: dataArray}
    )
  }

  fetchJson() {
    return fetch("http://127.0.0.1:8000/api/cases/")
          .then(response => response.json())
          .then(jsonArray => this.populateJson(jsonArray))
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
        // TODO Set default to 10 rows or infinite
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
