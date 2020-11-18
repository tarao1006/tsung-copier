window.addEventListener(
  'load',
  () => {
    addId();
    const footer = document.getElementsByTagName('footer')[0];
    const copyButton = document.createElement('button');
    copyButton.value = 'copy';
    copyButton.textContent = 'Copy'
    copyButton.onclick = copyTable;
    footer.appendChild(copyButton);
  }
)


const IDS = [
    'stats',
    'transaction',
    'network',
    'count',
    'errors',
    'os_mon',
    'http_status',
]


const printSuccessRate = statsTable => {
  let results = {};
  for (let i = 0; i < statsTable.values.length; ++i) {
    const tds = statsTable.values[i]

    let status;
    let highestRate;
    let meanRate;
    let totalNumber;
    for (let j = 0; j < tds.length; ++j) {
      if (j === 0) {
        status = tds[j];
      } else if (j === 1) {
        highestRate = parseFloat(tds[j].split(" ")[0]);
      } else if (j == 2) {
        meanRate = parseFloat(tds[j].split(" ")[0]);
      } else {
        totalNumber = parseInt(tds[j]);
      }
    }
    results[status] = {
      status,
      highestRate,
      meanRate,
      totalNumber
    }
  }

  let total = 0;
  let total_2xx = 0;
  let total_5xx = 0;

  for (const [key, value]of Object.entries(results)) {
    total += value.totalNumber;
    if (key.startsWith('2')) {
      total_2xx += value.totalNumber;
    } else if (key.startsWith('5')) {
      total_5xx += value.totalNumber;
    }
  }

  let rate;
  if (total_5xx == 0) {
    rate = '-'
  } else {
    rate = `${(total_2xx / total_5xx).toFixed(2)}`;
  }

  res = '## Calculated Values\n|Topic|Value|\n|:-:|:-:|\n';
  res += `|total_2xx|${total_2xx}|\n|total_5xx|${total_5xx}|\n`;
  res += `|2xx/5xx|${rate}|\n`;
  res += `|Success Rate|${(total_2xx / total).toFixed(2)}|\n`;

  return res;
}


const printElement = statsTable => {
  let header = '|';
  header += statsTable.header.join('|');
  header += '|\n'
  for (let i = 0; i < statsTable.header.length; ++i) {
    header += '|:-:'
  }
  header += '|\n'

  let values = ''
  for (const value of statsTable.values) {
    values += '|';
    values += value.join('|');
    values += '|\n';
  }
  values += '\n'

  return header + values;
}


const addId = () => {
  let elements = document.getElementsByTagName('h3');

  for (let element of elements) {
    if (element.textContent.trim() === "Errors") {
      element.id = 'errors';
    }
  }
}


const copyToClipBoard = txt => {
  let textarea = document.createElement('textarea');
  textarea.textContent = txt;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand('copy');
  document.body.removeChild(textarea);
}


const copyTable = () => {
  let txt = ''
  for (const id of IDS) {
    const ele = document.getElementById(id);
    if (ele === null) {
      continue;
    }
    
    txt += `## ${ele.textContent.trim()}\n`;

    const table_response = ele.nextSibling.nextSibling;
    const tables = table_response.getElementsByTagName('table');

    for (const table of tables) {
      let statsTable = {values: []};
      let trs = Array.from(table.getElementsByTagName('tr'));

      for (let i = 0; i < trs.length; ++i) {
        if (i === 0) {
          statsTable['header'] = Array.from(
            trs[i].getElementsByTagName('th'))
              .map(th => th.textContent.trim().replace("\n", ""));
        } else {
          statsTable['values'].push(Array.from(
            trs[i].getElementsByTagName('td'))
              .map(td => td.textContent.trim().replace("\n", "")));
        }
      }
      txt += printElement(statsTable);

      if (id === 'http_status') {
        txt += printSuccessRate(statsTable);
      }
    }
  }

  copyToClipBoard(txt);
}
