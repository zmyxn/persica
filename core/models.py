from django.db import models
import re
# Create your models here.


class TreeManager(models.Manager):
    def get_child(self, node):
        """ 返回Node的子节点 """
        return self.filter(parent=node)

    # def get_leaves(self, node=1):
    #     """ 返回以Node为根节点的树, 含自己 """
    #     node_group = re.findall(r'.{2}', str(node))
    #     node_id_pre = ''.join([x for x in node_group if x != '00'])
    #     node_id_max = "{:9<16}".format(node_id_pre)
    #     leaves = self.filter(models.Q(node__gte=node) & models.Q(node__lte=node_id_max))
    #     return leaves

    def get_leaves(self, node=1):
        """ 返回以node为根节点的树, 含自己 """
        node_list = [node]
        find_node = []
        while node_list:
            last_node = node_list.pop()
            find_node.append(last_node)
            for i in self.get_child(last_node):
                node_list.append(i.node)

        leaves = self.filter(node__in=find_node)
        return leaves

    def get_siblings(self, node):
        """ 返回Node的兄弟节点 """
        parent = self.filter(node=node).values("parent")
        return self.filter(parent=parent)

    def get_jstree(self, node=1):
        all_node = self.get_leaves(node)
        tree_root = {"id": all_node[0].node, "parent": "#", "text": all_node[0].name}
        data = [{"id": i.node, "parent": i.parent_id, "text": i.name} for i in all_node[1:]]
        data.append(tree_root)
        return data


class Tree(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name="node_name")
    node = models.BigIntegerField(primary_key=True, unique=True, verbose_name="node_id")
    parent = models.ForeignKey('self', on_delete=False, blank=True, null=True, verbose_name="parent_id")
    objects = TreeManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "树"
        ordering = ['node']