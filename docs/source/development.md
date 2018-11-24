# 项目规范

## 语言框架

- Python 3.6.6
- Django 1.11
- Ansible 

## 代码风格

Python 遵循 [PEP8][id]


## Django 规范

### 模型 
不同表中相同含义的字段名，尽可能统一  
> name 表示名称， 在不同的表中不要再带上前缀。  
> sub_name in model.domain   
> asset_name in model.asset  
> creatd 表示创建时间  
> 在不同表中出现create_time, create_data会  

### 视图

尽可能Class-based views

### 路由 

必须URL 独立命名

### 测试

尽可能用例完整



[id]: https://www.python.org/dev/peps/pep-0008/