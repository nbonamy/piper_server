module.exports = {
  apps : [{
    name: "piper-server",
    cmd: "main.py",
    interpreter: "python3",
    watch: true,
    watch_delay: 1000,
    log_date_format: "YYYY-MM-DD HH:mm:ss"
  }]
}
