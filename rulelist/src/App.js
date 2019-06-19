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
        { title: 'Defense', field: 'defense' , editable: 'onUpdate' },

        { title: 'Notes', field: 'notes', editable: 'onUpdate' },
        
        { title: 'Witness List', field: '1', type: 'date', editable: 'never' },
        { title: 'Scheduling Conference', field: '2', type: 'date', editable: 'never' },
        { title: 'Request PTIs', field: '3', type: 'date', editable: 'never' },
        { title: 'Conduct PTIs', field: '4', type: 'date', editable: 'never' },
        { title: 'Witness PTIs', field: '5', type: 'date', editable: 'never' },
        { title: 'Scientific Evidence', field: '6', type: 'date', editable: 'never' },
        { title: 'Pretrial Conference', field: '7', type: 'date', editable: 'never' },
        { title: 'Final Witness List', field: '8', type: 'date', editable: 'never' },
        { title: 'Need for Interpreter', field: '9', type: 'date', editable: 'never' },
        { title: 'Plea Agreement', field: '10', type: 'date', editable: 'never' },
        { title: 'Trial', field: '11', type: 'date', editable: 'never' },

      ],
      data: [
        { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz', 
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz', 
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz', 
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz', 
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz', 
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },
      ]
    }
  }

  testFetch() {
    return fetch("http://127.0.0.1:8000/api/deadlines/2/")
          .then(response => response.json())
          .then(json => console.log(json['datetime']))
  }

  render() {
    this.testFetch()
    return (
      
      <MaterialTable
        title="Rule List"
        columns={this.state.columns}
        data={this.state.data}
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
