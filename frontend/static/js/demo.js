// 切换放大/缩小
function toggleResize(element, type) {
  let target = element.closest("." + type + "-box");

  const icon = element.querySelector(".material-icons");

  // 切换放大缩小状态
  if (target.classList.contains("enlarged")) {
    target.classList.remove("enlarged");
    icon.textContent = "fullscreen"; // 切换回放大图标
    // 恢复所有的图表到 gauge
    const gaugesContainer = document.querySelector('.gauges-container');
    const allChartsContainer = document.querySelector('.all-charts-container');
    const analysisContent = document.querySelector(".analysis-content");

    if (gaugesContainer) {
      gaugesContainer.style.display = 'flex';
    }

    if (allChartsContainer) {
      allChartsContainer.style.display = 'none';
    }
    if (analysisContent) {
      analysisContent.style.display = "flex";
    }
  } else {
    // 关闭其他已放大的部分
    document.querySelectorAll(".enlarged").forEach((enlargedElement) => {
      enlargedElement.classList.remove("enlarged");
      const enlargedIcon = enlargedElement.querySelector(".resize-toggle .material-icons");
      if (enlargedIcon) {
        enlargedIcon.textContent = "fullscreen"; // 切换回放大图标
      }
    });

    // 放大当前部分
    target.classList.add("enlarged");
    icon.textContent = "fullscreen_exit"; // 切换到缩小图标

    // 如果是 analysis 部分, 则隐藏 gauge，显示所有图表
    if (type === "section" && target.classList.contains("analysis-section")) {
      const gaugesContainer = document.querySelector('.gauges-container');
      const allChartsContainer = document.querySelector('.all-charts-container');
      const analysisSection = document.querySelector('.analysis-section');
      const analysisContent = document.querySelector(".analysis-content");
      if (gaugesContainer) {
        gaugesContainer.style.display = 'none';
      }

      if (allChartsContainer) {
        allChartsContainer.style.display = 'block';
        analysisSection.style.overflow = 'auto';
        analysisContent.style.display = "block";
      }
    }
  }
}

// 发送按钮的加载状态及中断
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
  document.getElementById("vector-content").innerHTML = data.vectorResult;
  document.getElementById("vector-placeholder").style.display = "none";

  document.getElementById("graph-content").innerHTML = data.graphResult;
  document.getElementById("graph-placeholder").style.display = "none";

  document.getElementById("vector-answer-content").innerText = data.vectorAnswer;
  document.getElementById("graph-answer-content").innerText = data.graphAnswer;
  document.getElementById("hybrid-answer-content").innerText = data.hybridAnswer;

  // 更新分析参数，确保数据存在
  document.getElementById("analysis-content").innerText = data.analysisParams
    ? `Count: ${data.analysisParams.count}, Other Params: ${JSON.stringify(
        data.analysisParams.other
      )}`
    : "No parameters available";

  document.getElementById("advice-content").innerText = data.advice;
  updateGauges(data.gaugeData);
  initializeCharts(data.chartData);
}

// 下拉菜单的当前选中项
let activeDropdowns = {};

// 下拉菜单点击事件
document.querySelectorAll(".dropbtn").forEach((button) => {
  button.addEventListener("click", () => {
    const type = button.dataset.type;

    // 如果已经有选中的选项，并且不是当前的下拉菜单，则先关闭其他下拉菜单
    if (activeDropdowns[type]) {
      document.querySelectorAll(".dropdown-content").forEach((dropdown) => {
        dropdown.style.display = "none";
      });
    }

    // 切换当前下拉菜单的显示状态
    const dropdownContent = button.nextElementSibling;
    dropdownContent.style.display =
      dropdownContent.style.display === "block" ? "none" : "block";

    // 更新当前选中的下拉菜单
    activeDropdowns[type] = !activeDropdowns[type];
  });
});

// 下拉菜单选项点击事件
document.querySelectorAll(".dropdown-content a").forEach((item) => {
  item.addEventListener("click", () => {
    const type = item.closest(".dropdown").querySelector(".dropbtn").dataset.type;
    const subtype = item.dataset.subtype;

    // 更新按钮文本为选中的选项
    const button = item.closest(".dropdown").querySelector(".dropbtn");
    button.textContent = `${type.charAt(0).toUpperCase() +
      type.slice(1)}: ${subtype} ▼`;

    // 关闭下拉菜单
    item.closest(".dropdown-content").style.display = "none";

    console.log(`Fetching data for ${type} - ${subtype}...`);
    // 这里可以根据 type 和 subtype 发送请求到后端，获取对应的数据
    // 更新 UI，例如显示对应 type 和 subtype 的内容，隐藏其他内容
  });
});

function selectPreference(type) {
  // 移除所有已选中的偏好图标
  document
    .querySelectorAll(".preference-icon.selected")
    .forEach((icon) => {
      icon.classList.remove("selected");
    });

  // 为当前选中的类型添加选中状态
  if (type === "vector") {
    document
      .getElementById("vector-answer")
      .querySelector(".preference-icon")
      .classList.add("selected");
  } else if (type === "graph") {
    document
      .getElementById("graph-answer")
      .querySelector(".preference-icon")
      .classList.add("selected");
  } else if (type === "hybrid") {
    document
      .getElementById("hybrid-answer")
      .querySelector(".preference-icon")
      .classList.add("selected");
  }
}

// 新增：History 部分的逻辑
const datasetSelect = document.getElementById("dataset-select");
const questionList = document.getElementById("question-list");

// 模拟数据集数据
const datasets = {
  dataset1: [
    { id: 1, question: "What is the capital of France?", answer: "Paris", correct: true },
    { id: 2, question: "What is the highest mountain in the world?", answer: "Mount Everest", correct: true },
    { id: 3, question: "Who painted the Mona Lisa?", answer: "Michelangelo", correct: false },
  ],
  dataset2: [
    { id: 4, question: "What is the smallest country in the world?", answer: "Vatican City", correct: true },
    { id: 5, question: "What is the largest ocean in the world?", answer: "Atlantic Ocean", correct: false },
    { id: 6, question: "Who wrote Hamlet?", answer: "William Shakespeare", correct: true }
  ]
};

// 初始化数据集选项
for (const dataset in datasets) {
  const option = document.createElement("option");
  option.value = dataset;
  option.text = dataset;
  datasetSelect.add(option);
}

// 数据集选择事件
datasetSelect.addEventListener("change", () => {
  const selectedDataset = datasetSelect.value;
  displayQuestions(selectedDataset);
});

// 显示问题列表
function displayQuestions(dataset) {
  questionList.innerHTML = ""; // 清空问题列表

  if (datasets[dataset]) {
    datasets[dataset].forEach(item => {
      const questionItem = document.createElement("div");
      questionItem.classList.add("question-item");
      if (item.correct) {
        questionItem.classList.add("correct");
      } else {
        questionItem.classList.add("wrong");
      }
      questionItem.innerHTML = `
        <p>ID: ${item.id}</p>
        <p>Question: ${item.question}</p>
        <p>Answer: ${item.answer}</p>
      `;
      questionList.appendChild(questionItem);
    });
  }
}
// 更新仪表盘数据
function updateGauges(data) {
    if (data && data.length === 4) {
        createGauge('gauge1', data[0] * 100, 'percentage1');
        createGauge('gauge2', data[1] * 100, 'percentage2');
        createGauge('gauge3', data[2] * 100, 'percentage3');
        createGauge('gauge4', data[3] * 100, 'percentage4');
        // 大图
        createGauge('gauge1-big', data[0] * 100, 'percentage1-big');
        createGauge('gauge2-big', data[1] * 100, 'percentage2-big');
        createGauge('gauge3-big', data[2] * 100, 'percentage3-big');
        createGauge('gauge4-big', data[3] * 100, 'percentage4-big');
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
    // 饼图
    createPieChart(document.getElementById('pieChart1').getContext('2d'), data.pieChart1 || [10, 20, 30, 40]);
    createPieChart(document.getElementById('pieChart2').getContext('2d'), data.pieChart2 || [15, 25, 35, 25]);
    createPieChart(document.getElementById('pieChart3').getContext('2d'), data.pieChart3 || [5, 50, 25, 20]);
    createPieChart(document.getElementById('largePie').getContext('2d'), data.largePie || [10, 30, 20, 40]);

    // 雷达图
    createRadarChart(document.getElementById('radarChart1').getContext('2d'), ['指标1', '指标2', '指标3', '指标4', '指标5'], data.radarChart1 || [6, 7, 8, 5, 6]);
    createRadarChart(document.getElementById('radarChart2').getContext('2d'), ['指标1', '指标2', '指标3', '指标4', '指标5'], data.radarChart2 || [5, 6, 7, 6, 5]);
    createRadarChart(document.getElementById('radarChart3').getContext('2d'), ['指标1', '指标2', '指标3', '指标4', '指标5'], data.radarChart3 || [7, 8, 6, 5, 7]);
    createRadarChart(document.getElementById('radarChart4').getContext('2d'), ['指标1', '指标2', '指标3', '指标4', '指标5'], data.radarChart4 || [6, 7, 8, 5, 6]);
}

// 饼图创建函数
function createPieChart(ctx, data) {
    return new Chart(ctx, {
        type: 'pie',
        data: {
            datasets: [{
                data: data,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
            }],
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
            }
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
            scale: {
                ticks: {
                    beginAtZero: true,
                    max: 10,
                    stepSize: 1
                }
            }
        }
    });
}