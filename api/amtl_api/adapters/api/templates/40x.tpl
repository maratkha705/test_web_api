<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>$status_code: $detail</title>
        <style>
            html {height: 100%}
            body {
                font-family: Tahoma,Verdana,Segoe,sans-serif; font-size:14px;
                margin: 1px 0; padding: 1px 0;
                display: grid;
                height: 100%;
                grid-template-rows: auto 1fr auto;
                grid-template-areas: 'header' 'main' 'footer';
                overflow: hidden;
            }
            h1 {font-size:1.425em}
            main, header, footer {
                display:block;
                margin: -1px auto;
                width: 100%;
                border: #ccc 1px solid;
                padding: 11px;
                min-height: 60px;
                line-height: 22px;
                overflow-x: auto;
                box-sizing: border-box;
            }
            main {
                border: #ccc 1px solid;
            }
            header {
                border: #27ae60 1px solid;
                background-color: #27ae60;
                color: #fff;
            }
            footer {
                border: #2e4053 1px solid;
                background-color: #2e4053;
                color: #fff;
            }
        </style>
    </head>
    <body>
        <header></header>
        <main>
        <h1>$status_code: $detail</h1>
        <p>Url: $url</p>
        <p>На <a href="/">главную</a></p>
        </main>
        <footer></footer>
        <script src="/public/js/40x.min.js"></script>
    </body>
</html>
