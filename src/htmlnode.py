

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict[str, str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        class_name = type(self).__name__
        result = f"{class_name}({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})" 
        return result

    def __eq__(self, other: HTMLNode) -> bool:
        result1 = self.tag == other.tag
        result2 = self.value == other.value
        result3 = self.children == other.children
        result4 = self.props == other.props
        return result1 and result2 and result3 and result4

    def __ne__(self, other: HTMLNode) -> bool:
        result1 = self.tag != other.tag
        result2 = self.value != other.value
        result3 = self.children != other.children
        result4 = self.props != other.props
        return result1 or result2 or result3 or result4      

    def to_html(self) -> None:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props == None or self.props == "":
            return ""
        
        props_keys = self.props.keys()
        attribute_str = ""
        for prop_key in props_keys:
            attribute_str += f' {prop_key}="{self.props[prop_key]}"'
        return attribute_str   

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None) -> None:       
        super().__init__(tag=tag, value=value, props=props)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        result = f"{class_name}({self.tag!r}, {self.value!r}, {self.props!r})" 
        return result        

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value
        if self.props == None:
            result = f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            props_keys = self.props.keys()
            attribute_str = ""
            for prop_key in props_keys:
                attribute_str += f' {prop_key}="{self.props[prop_key]}"'
            result = f"<{self.tag}{attribute_str}>{self.value}</{self.tag}>"
        return result 




