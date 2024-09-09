<div>
    <h2 align="center">Real-time Facial Recognition Based Attendance and Activity Tracking System</h2>
</div>
<!--
<p align="center"><em>Abdisa Merga and Ephrata Zerfu</em></p>
<p align="center"></p>
-->
<h4><p align="Center">The Architecture</p></h4>
<div align="center">
    <a href="https://github.com/abdimk/facial_analysis/blob/main/Architecture"><img src="https://github.com/abdimk/facial_analysis/blob/main/Architecture/1.png" width="900"></a>
</div>


<p align="center">
<a target="_blank" href="https://search.maven.org/artifact/com.webencyclop.core/mftool-java"><img src="https://img.shields.io/maven-central/v/com.webencyclop.core/mftool-java.svg?label=Maven%20Central"/></a> 
<a target="_blank" href="https://www.codacy.com/gh/ankitwasankar/mftool-java/dashboard?utm_source=github.com&utm_medium=referral&utm_content=ankitwasankar/mftool-java&utm_campaign=Badge_Coverage"><img src="https://app.codacy.com/project/badge/Coverage/0054db87ea0f426599c3a30b39291388" /></a>
<a href="https://www.codacy.com/gh/ankitwasankar/mftool-java/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ankitwasankar/mftool-java&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/0054db87ea0f426599c3a30b39291388"/></a>
<a target="_blank" href="https://github.com/ankitwasankar/mftool-java/blob/master/license.md"><img src="https://camo.githubusercontent.com/8298ac0a88a52618cd97ba4cba6f34f63dd224a22031f283b0fec41a892c82cf/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f73656c656e69756d2d776972652e737667" /></a>
&nbsp <a target="_blank" href="https://www.linkedin.com/in/ankitwasankar/"><img height="20" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
</p>
<p align="center">
  This repository contains the <strong>Setup and Configration</strong> for activity and facial recogniton attendance system its also easy to setup.
    
  </p>

<p align="center">
<a href="#introduction">Introduction</a> &nbsp;&bull;&nbsp;
<a href="#installation">Installation</a> &nbsp;&bull;&nbsp;
<a href="#usage">Usage</a> &nbsp;&bull;&nbsp;
<a href="#documentation">Documentation</a> &nbsp;&bull;&nbsp;
<a href="#issue">Issue?</a>
</p>




# Introduction
This <b>repository</b> provides simple APIs/functions/methods to work with svm facial recogniton You can:

- Reconize faces using svm Classification [Tensorflow](for Future)
- Able to take live stream feeds from multiple cameras at the same time using Kafka
- Fetch historic data on kibana
- Fetch assocated details from the sqlite database
- Generate Historical report using csv
- Able to run on distributed system/cluster nodes

# Face recognition Process using svm(support vector machine) clssification
<h4><p align="Center">Face Recognition Process </p></h4>
<div align="center">
    <a href="https://github.com/abdimk/facial_analysis/blob/main/Architecture"><img src="https://github.com/abdimk/facial_analysis/blob/main/Architecture/2.png" width="900"></a>
</div>
## Installation

you need to Install those dependency for your os to run this system !

- Kafka - is a distributed event streaming platform used for building real-time data pipelines and streaming applications.
- ElasticSearch -is a distributed, RESTful search and analytics engine built on top of Apache Lucene.
- Kibana - Kibana is an open-source data visualization and exploration tool for Elasticsearch.
  
##### Graddle
```
implementation 'com.webencyclop.core:mftool-java:1.0.4'
```
For other dependency management tool, please visit
<a href="https://search.maven.org/artifact/com.webencyclop.core/mftool-java">https://search.maven.org/artifact/com.webencyclop.core/mftool-java</a>


## Usage
Sample code that shows how to use the library:<br/>
```
MFTool tool = new MFTool();
tool.matchingScheme("Axis");   //-- get a list of all schemes with Axis in its name
tool.getCurrentNav("120503");  //-- get current nav
```
The other available methods are described in the next section.

## Documentation
Multiple methods provide ways to work with mutual funds and related data. Those are listed below in detail.

### 1. How to initialize an MFTool object
```
MFTool tool = new MFTool();
```
This will create the object for you, but it's recommended that you create this object as a <b>singleton</b> object.
The object uses a caching mechanism, which under-the-hood caches the values of historic nav and other static information to improve the performance. 
<br/>If you are using the Spring project, you can create the bean in ``@Configuration`` configuration class.
```
@Configuration
public class MFToolConfig{
    @Bean
    public MFTool initializeMfTool() {
        MFTool tool = new MFTool();
        return tool;
    }
}
```
You can use MFTool in other services using ``@Inject`` or ``@autowired`` annotation.
```
@Service
public class MyService {
    
    @Autowired
    private MFTool tool;

    public void getCurrentNav(String scheme) {
        BigDecimal nav = tool.getCurrentNav(scheme);
    }
}
```
