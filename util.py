class StrUtil():
    @staticmethod
    def rmOperand(string):
        """rmOperand: 去除LaTeX使用的操作符
        ```
        '#$%{}~_^&' -> ''
        ```
        """
        invalidChar = r'#$%}{~_^\&'
        validify = str.maketrans(dict(zip(invalidChar, ('',)*len(invalidChar))))
        result = string.translate(validify)
        return result
    
    @staticmethod
    def caption(string):
        """caption: 转换为图片标题/说明文字
        ```
        'some-te#xt-h{er}e' -> 'Some text here'
        ```
        """
        result = string.replace('-', ' ').replace('_', ' ')
        result = StrUtil.rmOperand(result)
        result = result.capitalize()
        return result

    @staticmethod
    def label(string):
        """label: 转换为标签文字
        ```
        '$some tex&t_here' -> 'some-text-here'
        ```
        """
        result = string.replace(' ', '-').replace('_', '-')
        result = StrUtil.rmOperand(result)
        
        return result

    @staticmethod
    def fileName(string):
        """fileName: 转换为文件名
        ```
        'a <>/\\|:.\"*? File Name' -> 'a-file-name'
        ```
        """
        invalidChar = r'<>/\|:"*?.'
        validify = str.maketrans(dict(zip(invalidChar, ('',)*len(invalidChar))))
        result = string.translate(validify)
        result = result.strip()
        result = result.replace(' ', '-').replace('_', '-')
        result = StrUtil.rmOperand(result)
        return result