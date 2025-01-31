document.getElementById("login-form").addEventListener("submit", function (e) {
    e.preventDefault();  // 阻止默认的表单提交行为

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // 表单验证
    if (!username || !password) {
        alert("用户名和密码是必需的！");
        return;
    }

    const data = {
        username: username,
        password: password
    };

    // 使用 Fetch API 提交登录数据
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)  // 将数据转换为 JSON 格式
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);  // 显示成功信息
                window.location.href = '/';  // 假设登录成功后跳转到主页
            } else {
                alert(data.error);  // 显示错误信息
            }
        })
        .catch(error => console.error('Error:', error));
});
