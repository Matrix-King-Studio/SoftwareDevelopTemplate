# [项目名称]-前端

本项目后端基于 Matrix 工作室 Vue 项目模板创建，提前内置了 ElementPlus 等第三方开发库，可以极大的提高开发效率，避免重复造轮子。

## 快速开始

```shell
npm install
```

```shell
npm run dev
```

## 自动化测试

前端开发完成之后需要进行充分的测试，但是为了避免人工手动操作这种繁琐的方式，我们采用了 [playwright](https://www.npmjs.com/package/playwright) 进行自动化测试。

前面执行完了 `npm install` 之后，playwright 就已经安装好了，但是为了自动化操作，还需要手动安装一下浏览器插件。

```shell
npx playwright install
```
