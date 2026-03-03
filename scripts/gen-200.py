import re, json, pathlib
root = pathlib.Path(r"E:\\code\\AI-Articles")
md = root / "interview/cpp-qt/2026-03-03/questions.md"
text = md.read_text(encoding='utf-8')

entries = []
current_section = None
current_difficulty = None
for line in text.splitlines():
    line = line.strip()
    if line.startswith('## C++'):
        current_section = 'C++'
    elif line.startswith('## Qt'):
        current_section = 'Qt'
    elif line.startswith('### 简单'):
        current_difficulty = 'easy'
    elif line.startswith('### 稍难'):
        current_difficulty = 'medium'
    elif line.startswith('### 较难'):
        current_difficulty = 'hard'
    m = re.match(r"\d+\. \*\*Q:\*\* (.+)", line)
    if m:
        q = m.group(1)
        entries.append({'section': current_section, 'difficulty': current_difficulty, 'question': q, 'answer': ''})
        continue
    m2 = re.match(r"\*\*A:\*\* (.+)", line)
    if m2 and entries:
        entries[-1]['answer'] = m2.group(1)
        continue
    m3 = re.match(r"\*\*解释：\*\* (.+)", line)
    if m3 and entries:
        entries[-1]['answer'] += "\n解释：{}".format(m3.group(1))

base = []
for i,e in enumerate(entries, start=1):
    base.append({
        'id': "base-{}".format(i),
        'difficulty': e['difficulty'] or 'medium',
        'topic': e['section'],
        'question': e['question'],
        'answer': e['answer'].strip() or '（略）'
    })

extra = []

def add(idx, topic, q, a, diff):
    extra.append({'id': "extra-{}".format(idx), 'difficulty': diff, 'topic': topic, 'question': q, 'answer': a})

cpp = [
    ("C++ 模板", "解释模板实例化的时机与 ODR 常见问题", "模板在使用点实例化；跨翻译单元需避免多重定义冲突。常见做法是把模板实现放头文件，或显式实例化。", 'hard'),
    ("C++ 语义", "解释拷贝消除（RVO/NRVO）及其对移动语义的影响", "编译器可直接在目标位置构造对象，省去拷贝/移动。即使有移动构造，RVO 仍可消除临时对象。", 'medium'),
    ("C++ 并发", "解释内存序（memory_order）中 acquire/release 的用途", "release 保证之前写入对后续 acquire 可见；acquire 防止之后读写重排。用于无锁同步的“发布-获取”。", 'hard'),
    ("C++ 容器", "vector 与 deque 在随机访问与插入性能上的区别", "两者随机访问 O(1)，但 deque 分段存储，头尾插入更快；vector 连续内存更利于缓存与 SIMD。", 'medium'),
    ("C++ 异常", "如何实现强异常安全的赋值运算符？", "使用拷贝并交换（copy-and-swap）：先拷贝临时对象，成功后交换资源。失败不影响原对象状态。", 'hard'),
    ("C++ 类型系统", "解释“顶层 const/底层 const”区别", "顶层 const 修饰对象本身，底层 const 修饰所指向对象。模板/auto 推导会丢弃顶层 const。", 'medium'),
    ("C++ 对象模型", "解释虚继承解决什么问题、代价是什么", "虚继承解决菱形继承中的共享基类重复问题；代价是额外指针与运行时偏移计算。", 'hard'),
    ("C++ 资源管理", "unique_ptr 自定义删除器的作用与实现", "可管理非 new 资源（FILE*、句柄），通过自定义 deleter 指定释放方式。", 'medium'),
    ("C++ STL", "为什么 unordered_map 的迭代顺序不稳定？", "哈希桶分布与 rehash 会改变元素位置，插入/扩容会打乱顺序。", 'easy'),
    ("C++ 语言特性", "解释 explicit(bool) 在 C++20 中的用途", "可根据模板参数控制构造函数是否显式，提升泛型库的可用性与安全性。", 'hard'),
    ("C++ ABI", "不同编译器的 ABI 不兼容会带来哪些问题？", "对象布局、名称修饰、异常处理等不一致，导致链接或运行时崩溃。", 'medium'),
    ("C++ 编译", "头文件循环依赖如何解决？", "使用前置声明、拆分依赖、最小化 include 并采用 pImpl。", 'easy'),
    ("C++ 标准库", "string_view 的典型风险是什么？", "不拥有数据，底层字符串失效会导致悬空视图。需确保生命周期覆盖使用期。", 'medium'),
    ("C++ Lambda", "lambda 捕获方式的差异与风险", "值捕获复制对象，引用捕获依赖外部生命周期；可用 init-capture 做移动捕获。", 'medium'),
    ("C++ IO", "iostream 性能优化手段有哪些？", "关闭同步 `ios::sync_with_stdio(false)`，避免频繁 flush，必要时使用更低层 API。", 'easy'),
    ("C++ 多态", "纯虚函数与接口类的设计要点", "类含纯虚函数即抽象类；接口类应有虚析构，尽量只暴露纯虚函数。", 'easy'),
    ("C++ RTTI", "dynamic_cast 的使用场景与代价", "用于安全向下转型；需要 RTTI 支持，有运行时检查开销。", 'medium'),
    ("C++ 宏", "为什么应减少宏使用？", "宏无作用域、无类型检查，易引发意外替换。可用 constexpr/inline/template 替代。", 'easy'),
    ("C++ 可见性", "解释命名空间别名的用途", "减少长命名空间前缀，提升可读性，避免冲突。", 'easy'),
    ("C++ 编译期", "解释 constexpr 函数的限制与用途", "函数体需满足编译期求值规则；用于常量计算、数组维度等。", 'medium'),
    ("C++ 线程", "std::thread 与 std::jthread 区别", "jthread 支持自动 join 与停止令牌，避免忘记 join/ detach。", 'medium'),
    ("C++ 并发", "互斥锁与自旋锁适用场景", "互斥锁适合长临界区；自旋锁适合短临界区避免上下文切换。", 'hard'),
    ("C++ 容器", "list 与 forward_list 的区别", "list 双向链表，forward_list 单向链表，内存更省但功能少。", 'easy'),
    ("C++ 性能", "解释缓存友好与数据局部性", "连续内存布局提高缓存命中率，减少内存访问延迟。", 'medium'),
    ("C++ 构造", "成员初始化顺序由什么决定？", "由声明顺序决定，与初始化列表顺序无关。", 'easy'),
    ("C++ 运算符", "为什么建议实现移动赋值时处理自赋值？", "虽然右值自赋值较少，但防御性检查可避免异常情况造成资源破坏。", 'medium'),
    ("C++ 编译", "什么是 PIMPL？优缺点？", "将实现隐藏到指针指向的实现类，减少编译依赖但引入间接访问开销。", 'medium'),
    ("C++ 语言特性", "concepts 的作用是什么？", "对模板参数施加约束，提高错误信息质量与编译速度。", 'hard'),
    ("C++ 资源", "shared_ptr 的控制块包含哪些信息？", "包含强/弱引用计数、删除器、类型擦除信息等。", 'hard'),
    ("C++ 析构", "析构函数应避免抛异常的原因", "析构期间抛异常会导致 std::terminate，破坏异常安全。", 'easy'),
    ("C++ 字符串", "UTF-8 与 UTF-16 的优劣", "UTF-8 兼容 ASCII、英文高效；UTF-16 对中文/东亚字符更稳定但占用更大。", 'medium'),
    ("C++ 智能指针", "make_shared 的优势", "一次分配控制块+对象，减少内存碎片和分配次数。", 'medium'),
    ("C++ 编译", "翻译单元与链接的关系", "每个 .cpp 编译成目标文件，链接阶段解决符号并生成可执行。", 'easy'),
    ("C++ 容器", "unordered_map 什么时候退化为 O(n)？", "哈希冲突过多或遭遇恶意输入会退化；可自定义哈希降低风险。", 'hard'),
    ("C++ 异常", "异常传播与栈展开机制", "异常抛出后逐层销毁栈对象直到捕获；RAII 保障资源释放。", 'medium'),
    ("C++ 编译期", "如何理解 type_traits 的用途", "提供编译期类型判断/转换工具，如 is_integral、remove_reference。", 'medium'),
    ("C++ 语言特性", "范围 for 背后如何展开？", "编译器使用 begin/end 获取迭代器并循环，要求容器提供对应接口。", 'easy'),
    ("C++ 接口", "为什么 API 参数优先用 const 引用？", "避免拷贝开销，同时保证只读语义。", 'easy'),
    ("C++ 资源管理", "使用 unique_ptr 管理数组的注意点", "使用 unique_ptr<T[]> 并用 delete[]，且不提供 operator*。", 'medium'),
    ("C++ 算法", "stable_sort 与 sort 区别", "stable_sort 保持相等元素相对顺序，代价是额外空间与可能更慢。", 'medium'),
    ("C++ 编译", "什么是模块（C++20 modules）？", "替代头文件，提升编译速度与隔离性，但需要编译器支持。", 'hard'),
    ("C++ 内存", "解释对象的对齐填充如何影响 sizeof", "为满足对齐，编译器可能插入填充字节，从而增大结构体大小。", 'medium'),
    ("C++ 语言特性", "constexpr 与 consteval 的差异", "consteval 强制编译期求值；constexpr 允许运行期回退。", 'hard'),
    ("C++ 并发", "条件变量的典型用法与陷阱", "等待时需循环检查谓词，避免虚假唤醒。", 'medium'),
    ("C++ 资源", "为什么不推荐裸 new/delete？", "容易泄漏和异常安全问题，推荐 RAII + 智能指针。", 'easy'),
    ("C++ 指针", "nullptr_t 的类型性质是什么？", "是独立类型，可与指针安全比较，避免整型重载歧义。", 'easy'),
    ("C++ STL", "emplace_back 和 push_back 的区别", "emplace_back 原地构造，避免临时对象；push_back 先构造再移动/拷贝。", 'medium'),
    ("C++ 编译", "链接错误 undefined reference 常见原因", "函数只声明未定义、库未链接、模板未实例化。", 'easy'),
    ("C++ 设计", "Rule of 0 的核心思想", "尽量用标准库类型管理资源，让编译器生成默认特殊成员函数。", 'medium'),
    ("C++ 内存", "解释栈内存与堆内存差别", "栈管理自动、生命周期短；堆需手动管理，生命周期灵活但易泄漏。", 'easy'),
    ("C++ 现代", "解释 std::span 的用途", "提供非拥有的连续序列视图，可安全传递数组/容器片段。", 'medium'),
    ("C++ 编译优化", "LTO（链接时优化）有什么优势？", "跨模块优化，提高性能但增加链接时间。", 'medium'),
]

qt = [
    ("Qt 事件", "解释事件循环在 Qt 中的角色", "事件循环负责派发事件与信号槽回调，GUI 线程必须运行事件循环以保持响应。", 'easy'),
    ("Qt UI", "QWidget 的绘制流程是什么？", "系统触发 paintEvent，开发者使用 QPainter 绘制；不建议在其他地方直接绘制。", 'medium'),
    ("Qt 资源", "QRC 资源系统在发布时的优势", "资源打包到可执行文件，避免路径丢失并简化部署。", 'easy'),
    ("Qt 样式", "QSS 与 QStyle 的区别和适用场景", "QSS 类 CSS，配置快速；QStyle 更底层更强大，适合深度定制。", 'medium'),
    ("Qt 模型", "QAbstractTableModel 中 data 的 role 应如何设计？", "用 DisplayRole 提供文本，UserRole 承载自定义数据，保持视图层解耦。", 'medium'),
    ("Qt 线程", "解释 QObject 的线程归属与事件处理", "QObject 归属线程由 moveToThread 决定，事件与槽在该线程处理。", 'medium'),
    ("Qt 信号槽", "连接信号槽返回值的意义", "connect 返回 bool，失败常因签名不匹配或对象已销毁。", 'easy'),
    ("Qt IO", "QIODevice 的抽象意义", "统一文件、网络、内存等 IO 接口，提供 open/read/write。", 'medium'),
    ("Qt 网络", "QNetworkReply 生命周期管理方式", "由 QNetworkAccessManager 创建，完成后可 deleteLater 或父对象管理。", 'medium'),
    ("Qt UI", "Qt 中布局与手动定位的差异", "布局自动适配尺寸与 DPI；手动定位易错且不适配多分辨率。", 'easy'),
    ("Qt 事件", "事件过滤器的典型用法", "用于全局快捷键、输入拦截、日志采集等场景。", 'medium'),
    ("Qt QML", "QML 中 property 与 signal 的作用", "property 绑定数据，signal 通知事件，二者用于声明式 UI。", 'easy'),
    ("Qt QML", "如何暴露 C++ 类型给 QML", "使用 qmlRegisterType 或 setContextProperty，结合 Q_PROPERTY。", 'medium'),
    ("Qt 多线程", "QtConcurrent 的适用场景", "适合并行计算/任务映射，避免手动线程管理。", 'medium'),
    ("Qt 调试", "QLoggingCategory 的优势", "支持分类与级别控制，便于过滤日志。", 'easy'),
    ("Qt 资源", "QFile 与 QFileInfo 的区别", "QFile 操作文件，QFileInfo 提供元信息（大小、时间、权限）。", 'easy'),
    ("Qt 视图", "QListView 与 QTableView 选择依据", "单列或简单列表用 QListView，多列/表格用 QTableView。", 'easy'),
    ("Qt 性能", "解释 Qt 中的隐式共享（COW）", "如 QString/QImage 使用共享计数，拷贝时只增计数，写时才复制。", 'medium'),
    ("Qt UI", "QMainWindow 的核心组成", "菜单栏、工具栏、状态栏、DockWidget 和中央窗口。", 'easy'),
    ("Qt 线程", "为什么禁止子线程操作 QWidget？", "GUI 不是线程安全，跨线程访问会导致崩溃或未定义行为。", 'easy'),
    ("Qt 绘图", "QPixmap 与 QImage 在性能上的差异", "QPixmap 更适合 GPU/显示，QImage 更适合 CPU 处理与 IO。", 'medium'),
    ("Qt 事件", "自定义事件的流程", "继承 QEvent，注册类型，重写 event() 处理。", 'medium'),
    ("Qt 组件", "QAction 的用途与优点", "可复用的命令对象，统一管理菜单、工具栏、快捷键。", 'easy'),
    ("Qt 表单", "QValidator 的工作方式", "在输入阶段验证与限制，减少后续错误处理。", 'easy'),
    ("Qt 系统", "QSettings 在不同平台的存储位置", "Windows 注册表，macOS plist，Linux ini/配置文件。", 'medium'),
    ("Qt 国际化", "动态切换语言的做法", "安装/卸载 QTranslator 并重新翻译 UI（retranslateUi）。", 'medium'),
    ("Qt 模型", "QSortFilterProxyModel 的作用", "在不改动源模型的情况下排序与过滤。", 'medium'),
    ("Qt QML", "QML 与 Widgets 混用的注意点", "性能与渲染栈不同，需谨慎管理输入与焦点。", 'hard'),
    ("Qt 线程", "QThread::quit() 与 exit() 的区别", "quit 发送退出事件结束事件循环；exit 可携带退出码。", 'medium'),
    ("Qt 网络", "同步网络请求的风险", "会阻塞 UI 线程，导致界面卡顿；应使用异步。", 'easy'),
    ("Qt UI", "QDockWidget 的典型使用场景", "IDE 类软件可停靠面板，提升可配置性。", 'easy'),
    ("Qt 模型", "模型数据更新的正确通知方式", "用 begin/endInsertRows、dataChanged 等通知视图更新。", 'hard'),
    ("Qt 事件", "窗口重绘的触发条件", "窗口尺寸变化、遮挡恢复、update() 调用都会触发。", 'easy'),
    ("Qt 图形", "QGraphicsView 性能优化手段", "减少 Item 数量，使用缓存，开启索引。", 'hard'),
    ("Qt 线程", "解释线程安全的 signal/slot 连接", "跨线程使用 queued connection，数据需线程安全。", 'medium'),
    ("Qt QML", "QML 中的 ListModel 与 C++ Model 区别", "ListModel 适合简单数据，复杂数据建议 C++ Model。", 'medium'),
    ("Qt 工程", "CMake 与 qmake 的差异", "CMake 更通用，qmake 为 Qt 旧构建系统。", 'easy'),
    ("Qt 资源", "大文件读取推荐的方式", "QFile + QDataStream 或分块读取，避免一次性加载。", 'medium'),
    ("Qt 组件", "QTableWidget 与 QTableView 区别", "Widget 是便利封装，View + Model 更灵活可扩展。", 'medium'),
    ("Qt UI", "高 DPI 适配策略", "使用自动缩放属性、布局自适应、避免硬编码像素。", 'medium'),
    ("Qt 日志", "Qt 中断言 Q_ASSERT 的作用", "调试期检查条件，发布版可被禁用。", 'easy'),
    ("Qt UI", "窗口无响应的常见原因", "主线程阻塞、死循环、频繁重绘或同步 IO。", 'easy'),
    ("Qt 事件", "QEvent::Type 自定义类型范围", "使用 QEvent::User 之后的值避免冲突。", 'medium'),
    ("Qt QML", "QML 绑定循环如何避免", "避免相互依赖的绑定，必要时使用 Binding 或中间变量。", 'hard'),
    ("Qt 网络", "HTTPS 证书错误处理方式", "监听 sslErrors 信号，谨慎忽略并提示用户。", 'hard'),
    ("Qt 线程", "moveToThread 后对象父子关系的限制", "对象必须无父对象，否则无法移动线程。", 'medium'),
    ("Qt UI", "自定义控件与事件处理流程", "重写 paintEvent/鼠标键盘事件，必要时调用基类实现。", 'medium'),
    ("Qt 工具", "Qt Designer 的适用范围", "适合快速布局 UI，复杂交互仍需代码控制。", 'easy'),
    ("Qt QML", "解释 QQmlEngine 与 QQmlApplicationEngine 区别", "前者是引擎核心，后者封装了加载 QML 的应用层逻辑。", 'medium'),
    ("Qt 性能", "QML 中性能优化的常用方法", "避免大量绑定、使用复用组件、减少重绘并合理使用 Loader。", 'hard'),
]

idx = 1
for t,q,a,d in cpp:
    add(idx, t, q, a, d); idx += 1
for t,q,a,d in qt:
    add(idx, t, q, a, d); idx += 1

# Trim/pad to 100 extras
extra = extra[:100]

allq = base + extra

final = []
for i, q in enumerate(allq, start=1):
    q['id'] = "q{:03d}".format(i)
    final.append(q)

out = root / "docs/public/data/2026-03-03.json"
out.write_text(json.dumps({'questions': final}, ensure_ascii=False, indent=2), encoding='utf-8')
print("Wrote {} questions to {}".format(len(final), out))
