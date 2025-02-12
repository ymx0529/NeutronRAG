const sendButton = document.getElementById("send-button");
let isGenerating = false;
let abortController = new AbortController();

sendButton.addEventListener("click", async () => {
  if (!isGenerating) {
    const userInput = document.getElementById("user-input").value;
    sendButton.textContent = "加载中...";
    sendButton.disabled = true;
    isGenerating = true;
    abortController = new AbortController();
    let signal = abortController.signal;

    try {
      const response = await fetch("/generate", {
        method: "POST",
        body: JSON.stringify({ input: userInput }),
        signal: signal,
      });

      if (response.ok) {
        const data = await response.json();
        updateUIWithResponse(data);
      } else {
        throw new Error("Network response was not ok.");
      }
    } catch (error) {
      if (error.name === "AbortError") {
        console.log("Fetch aborted");
      } else {
        console.error("Fetch error:", error);
      }
    } finally {
      sendButton.textContent = "发送";
      sendButton.disabled = false;
      isGenerating = false;
    }
  } else {
    abortController.abort();
    isGenerating = false;
    sendButton.textContent = "发送";
    sendButton.disabled = false;
  }
});

// 模拟后端数据更新UI
function updateUIWithResponse(data) {
  // 更新 Retrieval Result 部分
  document.getElementById("vector-content").innerHTML = "";
  if (data.vectorResult && data.vectorResult.length > 0) {
      document.getElementById("vector-placeholder").style.display = "none";
      data.vectorResult.forEach((item, index) => {
          const vectorResultItem = document.createElement("div");
          vectorResultItem.classList.add("retrieval-result-item");
          vectorResultItem.innerHTML = `
              <p><b>Chunk ${index + 1}:</b> ${item}</p>
          `;
          document.getElementById("vector-content").appendChild(vectorResultItem);
      });
  } else {
      document.getElementById("vector-placeholder").style.display = "flex";
  }

  document.getElementById("graph-content").innerHTML = "";
  if (data.graphResult && data.graphResult.length > 0) {
      document.getElementById("graph-placeholder").style.display = "none";
      data.graphResult.forEach((item, index) => {
          const graphResultItem = document.createElement("div");
          graphResultItem.classList.add("retrieval-result-item");
          graphResultItem.innerHTML = `
              <p><b>Chunk ${index + 1}:</b> ${item}</p>
          `;
          document.getElementById("graph-content").appendChild(graphResultItem);
      });
  } else {
      document.getElementById("graph-placeholder").style.display = "flex";
  }
  

  // 更新 Answer 部分
 document.getElementById("vector-answer-content").innerHTML = `
        <div class="question-container">
            <img src="./lib/employee.png" alt="Question Icon" class="question-icon">
            <p class="question-text">When was Pixel Fold announced?</p>
        </div>
        <div class="answer-text">
            <img src="./lib/llama.png" alt="Answer Icon" class="answer-icon-llama">
            According to the provided context information, Pixel Fold was announced on September 12, 2022.
        </div>
  `;
  document.getElementById("graph-answer-content").innerText = data.graphAnswer; // 这里需要根据实际数据更新
  document.getElementById("hybrid-answer-content").innerText = data.hybridAnswer; // 这里需要根据实际数据更新

  // 更新 Suggestions 部分
  document.getElementById("advice-content").innerHTML = `
    <ul class="advice-list">
        <li class="advice-item">
            <img src="./lib/advice.png" alt="Advice Icon" class="advice-icon">
            <span class="advice-text">Most of the errors are caused by lack useful information.</span>
        </li>
        <li class="advice-item">
            <img src="./lib/advice.png" alt="Advice Icon" class="advice-icon">
            <span class="advice-text"><b>VectorRAG:</b></span>
        </li>
        <li class="advice-item">
            <img src="./lib/advice.png" alt="Advice Icon" class="advice-icon">
            <span class="advice-text">Try to increase Chunksize</span>
        </li>
        <li class="advice-item">
            <img src="./lib/advice.png" alt="Advice Icon" class="advice-icon">
            <span class="advice-text">Increase the value of TOP-K</span>
        </li>
        <li class="advice-item">
            <img src="./lib/advice.png" alt="Advice Icon" class="advice-icon">
            <span class="advice-text"><b>GraphRAG:</b></span>
        </li>
        <li class="advice-item">
            <img src="./lib/advice.png" alt="Advice Icon" class="advice-icon">
            <span class="advice-text">Increase K-HOP value</span>
        </li>
    </ul>
  `;

  // 更新 Analysis 部分
  updateGauges(data.gaugeData);
  initializeCharts(data.chartData);
}

// 控制左侧栏各个部分折叠的函数
function toggleSidebarSection(header) {
    const content = header.nextElementSibling;
    header.classList.toggle("collapsed");
    if (content.style.display === "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}

// History 部分的逻辑
const questionList = document.getElementById("question-list");
let currentDataset = null;

// 模拟数据集数据
const datasets = {
  RGB: [
    { id: 1, question: "What is the capital of France?", answer: "Paris", correct: true },
    { id: 2, question: "What is the highest mountain in the world?", answer: "Mount Everest", correct: true },
    { id: 3, question: "Who painted the Mona Lisa?", answer: "Michelangelo", correct: false },
  ],
  Multihop: [
    { id: 4, question: "What is the smallest country in the world?", answer: "Vatican City", correct: true },
    { id: 5, question: "What is the largest ocean in the world?", answer: "Atlantic Ocean", correct: false },
    { id: 6, question: "Who wrote Hamlet?", answer: "William Shakespeare", correct: true }
  ],
    RAGAS: [
        { id: 7, question: "What is the capital of Italy?", answer: "Rome", correct: true },
        { id: 8, question: "What is the deepest lake in the world?", answer: "Lake Baikal", correct: true },
        { id: 9, question: "Who painted the Last Supper?", answer: "Leonardo da Vinci", correct: true },
    ],
    RAGEval: [
        { id: 10, question: "What is the longest river in the world?", answer: "Nile", correct: true },
        { id: 11, question: "What is the largest desert in the world?", answer: "Sahara Desert", correct: false },
        { id: 12, question: "Who wrote The Odyssey?", answer: "Homer", correct: true }
    ],
    "CRUD-RAG": [
        { id: 13, question: "What is the capital of Canada?", answer: "Ottawa", correct: true },
        { id: 14, question: "What is the highest waterfall in the world?", answer: "Angel Falls", correct: true },
        { id: 15, question: "Who painted The Starry Night?", answer: "Vincent van Gogh", correct: true },
    ],
    RECALL: [
        { id: 16, question: "What is the largest country in the world?", answer: "Russia", correct: true },
        { id: 17, question: "What is the smallest continent in the world?", answer: "Australia", correct: true },
        { id: 18, question: "Who wrote The Iliad?", answer: "Homer", correct: true }
    ]
};

// 显示问题列表
function displayQuestions(dataset) {
  questionList.innerHTML = ""; // 清空问题列表
  currentDataset = dataset;

  if (dataset && datasets[dataset]) {
    datasets[dataset].forEach(item => {
      const questionItem = document.createElement("div");
      questionItem.classList.add("question-item");
      if (item.correct) {
        questionItem.classList.add("correct");
        questionItem.innerHTML = `
          <img src="./lib/correct.png" alt="Correct Icon" class="question-icon">
          <p>id: ${item.id},  query: ${item.question} Ground truth: ${item.answer}</p>
        `;
      } else {
        questionItem.classList.add("wrong");
        questionItem.innerHTML = `
          <img src="./lib/wrong.png" alt="Wrong Icon" class="question-icon">
          <p>id: ${item.id},  query: ${item.question} Ground truth: ${item.answer}</p>
        `;
      }
      questionList.appendChild(questionItem);
    });
  } else {
      // 如果没有选择数据集，则显示提示信息
      questionList.innerHTML = "<p>Please select a dataset from the left sidebar.</p>";
  }
  updateHistoryTitle(dataset);
  addMoreButtonEventListeners();
}

// 更新 History 标题
function updateHistoryTitle(dataset = "") {
    const historyTitle = document.getElementById("history-title-text");
    historyTitle.textContent = `History: ${dataset}`;
}

// 为 More 按钮添加事件监听器
document.addEventListener('DOMContentLoaded', () => {
    const backButton = document.querySelector(".analysis-section .back-button");
    const analysisSection = document.querySelector('.analysis-section');

    if(backButton && analysisSection){
        backButton.addEventListener("click", function() {
            analysisSection.classList.remove("enlarged");
            analysisSection.style.display = "none";
        });
    }
  // 在 DOMContentLoaded 事件中调用 addMoreButtonEventListeners
  addMoreButtonEventListeners();
});

// 为 More 按钮添加事件监听器
function addMoreButtonEventListeners() {
  const moreButton = document.querySelector(".more-info .material-icons");
  const analysisSection = document.querySelector('.analysis-section');

  if (analysisSection) {
      moreButton.addEventListener("click", function(event) {
          event.stopPropagation();

          analysisSection.classList.toggle("enlarged");

          if (analysisSection.classList.contains("enlarged")) {
            analysisSection.style.display = "flex";
          } else {
            analysisSection.style.display = "none";
          }
      });
  } else {
      console.error("Error: .analysis-section element not found!");
  }
}

// 创建仪表盘的函数
function createGauge(elementId, percentage, textFiledId) {
    const isBig = elementId.includes('-big');
    var opts = {
        angle: 0.15,
        lineWidth: isBig? 0.33 : 0.22,
        radiusScale: isBig ? 0.9 : 1,
        pointer: {
            length: isBig ? 0.5 : 0.6,
            strokeWidth: isBig ? 0.025: 0.035,
            color: '#000000'
        },
        limitMax: false,
        limitMin: false,
        colorStart: '#B068CF',
        colorStop: '#8FC0DA',
        strokeColor: '#E0E0E0',
        generateGradient: true,
        highDpiSupport: true,
        staticZones: [
            {strokeStyle: "#F03E3E", min: 0, max: 20},
            {strokeStyle: "#FFDD00", min: 20, max: 50},
            {strokeStyle: "#30B32D", min: 50, max: 80},
            {strokeStyle: "#FFDD00", min: 80, max: 90},
            {strokeStyle: "#F03E3E", min: 90, max: 100}
        ],
        staticLabels: {
            font: isBig ? "16px sans-serif" : "10px sans-serif",
            labels: isBig ? [0, 20, 50, 80, 100] : [0, 20, 50, 80, 100],
            color: "#000000",
            fractionDigits: 0
        },
        renderTicks: {
            divisions: isBig ? 5 : 5,
            divWidth: isBig ? 0.9 : 1.1,
            divLength: isBig ? 0.6 : 0.7,
            divColor: '#333333',
            subDivisions: isBig ? 3 : 3,
            subLength: isBig ? 0.3 : 0.5,
            subWidth: isBig ? 0.4 : 0.6,
            subColor: '#666666'
        }
    };

    var target = document.getElementById(elementId);
    var gauge = new Gauge(target).setOptions(opts);
    gauge.maxValue = 100;
    gauge.setMinValue(0);
    gauge.animationSpeed = 32;
    gauge.set(percentage);
    gauge.setTextField(document.getElementById(textFiledId));
    return gauge;
}

// 初始化所有图表
function initializeCharts(data) {
    if (!data) {
        console.error("No chart data provided to initializeCharts");
        return;
    }
    console.log("Chart Data:", data); // 打印数据
    // 饼图
    console.log("pieChart1 context:", document.getElementById('pieChart1').getContext('2d'));  // 打印上下文
    createPieChart(document.getElementById('pieChart1').getContext('2d'), data.pieChart1 || [10, 20, 30, 40], ["None Result", "Lack Information", "Noisy", "Other"]);
    createPieChart(document.getElementById('pieChart2').getContext('2d'), data.pieChart2 || [15, 25, 35, 25], ["None Result", "Lack Information", "Noisy", "Other"]);
    createPieChart(document.getElementById('pieChart3').getContext('2d'), data.pieChart3 || [5, 50, 25, 20], ["None Result", "Lack Information", "Noisy", "Other"]);

    // 雷达图
    createRadarChart(document.getElementById('radarChart1').getContext('2d'), ['Accuracy', 'Relevance', 'Recall', 'Faithfulness'], data.radarChart1 || [0.6, 0.7, 0.8, 0.5]);
    createRadarChart(document.getElementById('radarChart2').getContext('2d'), ['Accuracy', 'Relevance', 'Recall', 'Faithfulness'], data.radarChart2 || [0.5, 0.6, 0.7, 0.6]);
    createRadarChart(document.getElementById('radarChart3').getContext('2d'), ['Accuracy', 'Relevance', 'Recall', 'Faithfulness'], data.radarChart3 || [0.7, 0.8, 0.6, 0.5]);
    const pieChart1 = document.getElementById('pieChart1');
    pieChart1.width = pieChart1.width;

    const radarChart1 = document.getElementById('radarChart1');
    radarChart1.width = radarChart1.width;
  }
  window.onload = function() {
    // 从后端获取数据
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            // 初始化图表
            initializeCharts(data);
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
};
// 饼图创建函数
function createPieChart(ctx, data, labels) {
    return new Chart(ctx, {
        type: 'pie',
        data: {
            datasets: [{
                data: data,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
                label: 'Dataset 1'
            }],
            labels: labels
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                datalabels: {
                    formatter: function(value, context) {
                        return value + '%'; // Show percentage on each section
                    },
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: 16
                    },
                    anchor: 'center', // 文字居中显示
                    align: 'center'   // 文字居中显示
                }
            },
            legend: {
                display: true, // 显示图例
                position: 'bottom', // 图例位置
            },
        },
        plugins: [ChartDataLabels]
        
    });
}

// 雷达图创建函数
function createRadarChart(ctx, labels, data) {
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: '评估指标',
                data: data,
                backgroundColor: 'rgba(34, 202, 236, 0.2)',
                borderColor: 'rgba(34, 202, 236, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    min: 0,
                    ticks: {
                        stepSize: 0.2
                    }
                }
            }
        }
    });
}

// RAG 模式切换逻辑
const ragSelect = document.getElementById("rag-select");
const vectorAnswerBox = document.getElementById("vector-answer");
const graphAnswerBox = document.getElementById("graph-answer");
const hybridAnswerBox = document.getElementById("hybrid-answer");

ragSelect.addEventListener("change", () => {
    const selectedRag = ragSelect.value;

    // 隐藏所有 RAG 答案
    vectorAnswerBox.style.display = "none";
    graphAnswerBox.style.display = "none";
    hybridAnswerBox.style.display = "none";

    // 显示选中的 RAG 答案
    if (selectedRag === "vector") {
        vectorAnswerBox.style.display = "block";
    } else if (selectedRag === "graph") {
        graphAnswerBox.style.display = "block";
    } else if (selectedRag === "hybrid") {
        hybridAnswerBox.style.display = "block";
    }
});

// 页面加载时, 将dataset的内容发送给后端, 保持history更新
document.addEventListener('DOMContentLoaded', () => {
  // 获取所有 dataset 选项的单选按钮
  const datasetRadios = document.querySelectorAll('input[name="dataset"]');

  // 默认不选中数据集
  // 为每个 dataset 单选按钮添加事件监听器
  datasetRadios.forEach(radio => {
      radio.addEventListener('change', () => {
          if (radio.checked) {
              const selectedDataset = radio.value;
              console.log(`Dataset selected: ${selectedDataset}`);
              // 在这里发送请求到后端，更新 history 部分
              displayQuestions(selectedDataset);
          }
      });
  });

  // 模型选择和 API-KEY 联动
  const modelSelect = document.getElementById("model-select");
  const apiKeyInput = document.getElementById("api-key-input");

  const modelApiKeys = {
      ModelA: "API-KEY-A",
      ModelB: "API-KEY-B",
      ModelC: "API-KEY-C",
  };

  // 初始设置 API-KEY
  apiKeyInput.value = modelApiKeys[modelSelect.value];

  modelSelect.addEventListener("change", () => {
      apiKeyInput.value = modelApiKeys[modelSelect.value];
  });

  // 在 DOMContentLoaded 事件中调用 addMoreButtonEventListeners
  addMoreButtonEventListeners();
});



// ### History显示question_list
document.getElementById('readButton').addEventListener('click', function() {
    fetch('/read-file', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const questionListDiv = document.getElementById('question-list');
        questionListDiv.innerHTML = '';  // 清空之前的输出

        if (data.content) {
            const list = data.content;

            // 使用 setTimeout 来模拟逐条添加
            let index = 0;
            const interval = setInterval(() => {
                if (index < list.length) {
                    const item = list[index];

                    // 创建一个新的 div 来包裹内容
                    const div = document.createElement('div');
                    div.classList.add('question-item');  // 为每个 div 添加一个类名，方便样式设置
                    div.id = item.id; // 将每个 div 设置为它的 ID，方便后端选择数据
                    
                    // 根据 item.type 为 div 设置背景色
                    switch (item.type) {
                        case 'GREEN':
                            div.style.backgroundColor = '#d9f7be';  // 浅绿色
                            break;
                        case 'RED':
                            div.style.backgroundColor = '#ffccc7';  // 浅红色
                            break;
                        case 'YELLOW':
                            div.style.backgroundColor = '#fff2e8';  // 浅橙色
                            break;
                        default:
                            div.style.backgroundColor = '#f0f0f0';  // 默认背景色
                            break;
                    }

                    // 创建一个 li 元素，并将内容放入
                    const li = document.createElement('li');
                    li.textContent = JSON.stringify(item, null, 2); // 美化显示 JSON

                    // 将 li 添加到 div 中
                    div.appendChild(li);

                    // 为 div 添加点击事件
                    div.addEventListener('click', function() {
                        const answerContentDiv = document.querySelector('.answer-content');
                        if (answerContentDiv) {
                            answerContentDiv.innerHTML = `
                                <strong>Query:</strong> ${item.question}<br>
                                <strong>Answer:</strong> ${item.answer}
                            `;

                            // 根据 div 的 ID，动态获取对应的 JSON 文件内容
                            const itemId = div.id;

                            // 请求第一个 JSON 文件（向量数据）
                            fetch(`/get-vector/${itemId}`, {
                                method: 'GET',
                                headers: { 'Content-Type': 'application/json' }
                            })
                            .then(response => response.json())
                            .then(vectorData => {
                                const vectorContentDiv = document.getElementById('vector-content');
                                vectorContentDiv.innerHTML = `<pre>${JSON.stringify(vectorData, null, 2)}</pre>`;
                            })
                            .catch(error => {
                                console.error('Error fetching vector data:', error);
                                alert('Error fetching vector data');
                            });

                            // 请求第二个 JSON 文件（图数据）
                            fetch(`/get-graph/${itemId}`, {
                                method: 'GET',
                                headers: { 'Content-Type': 'application/json' }
                            })
                            .then(response => response.json())
                            .then(graphData => {
                                const graphContentDiv = document.getElementById('graph-content');
                                graphContentDiv.innerHTML = `<pre>${JSON.stringify(graphData, null, 2)}</pre>`;
                            })
                            .catch(error => {
                                console.error('Error fetching graph data:', error);
                                alert('Error fetching graph data');
                            });
                        }
                    });

                    // 将整个 div 添加到 questionListDiv
                    questionListDiv.appendChild(div);

                    // 让容器自动滚动到底部
                    questionListDiv.scrollTop = questionListDiv.scrollHeight;

                    index++;
                } else {
                    clearInterval(interval);  // 清除定时器，停止添加
                }
            }, 1000); // 每秒添加一个新的列表项
        } else {
            alert('No content returned');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error reading file');
    });
});
