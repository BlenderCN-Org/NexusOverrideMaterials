bl_info = {
	"name": "Nexus Override Materials",
	"author": "Nexus Studio",
	"version": (0, 1, 0),
	"blender": (2, 80, 0),
	"location": "Properties > View Layers",
	"description": "Tools for fast override materials in selected objects (MESH)",
	"warning": "",
	"wiki_url": "https://github.com/Hichigo/NexusOverrideMaterials",
	"category": "Material"
	}

import bpy

from bpy.props import (IntProperty,
											 BoolProperty,
											 StringProperty,
											 CollectionProperty,
											 PointerProperty)

from bpy.types import (Operator,
											 Panel,
											 PropertyGroup,
											 UIList)

# -------------------------------------------------------------------
#   Functions
# -------------------------------------------------------------------

def CheckExistIndex(indexMat):
	i = 0

	for idx in bpy.context.scene.exludeIndexes:
		if idx.arrayIndex == indexMat:
			return True, i

		i += 1

	return False, -1


# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class NOM_OT_ExcludeMat(bpy.types.Operator):

	bl_idname = "exclude.material"
	bl_label = "Exclude material"

	index = bpy.props.IntProperty(
		name="Index material",
		description="Index material",
		default=-1
	)

	def execute(self, context):
		print(bpy.data.materials[self.index])

		remove, removeIdx = CheckExistIndex(self.index)
		if remove:
			bpy.context.scene.exludeIndexes.remove(removeIdx)
			print('remove', removeIdx)
		else:
			new_item = bpy.context.scene.exludeIndexes.add()
			new_item.arrayIndex = self.index
			print('add', self.index)

		return {'FINISHED'}


# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------

class NOM_UL_items(UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		mat = item

		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			row = layout.row(align=True)
			row.prop(mat, "name", text="", emboss=False, icon_value=layout.icon(mat))
			
			remove, removeIdx = CheckExistIndex(index)
			if remove:
				iconName = 'CANCEL'
			else:
				iconName = 'FILE_TICK'
			row.operator("exclude.material", icon=iconName, text="").index = index

	def invoke(self, context, event):
		pass

class NOM_PT_objectList(Panel):
	"""Adds a custom panel to the TEXT_EDITOR"""
	bl_idname = 'NOM_PT_ListMaterials'
	bl_space_type = "PROPERTIES"
	bl_region_type = 'WINDOW'
	bl_context = "view_layer"
	bl_label = "Nexus Override Materials"

	def draw(self, context):
		layout = self.layout
		scn = bpy.context.scene
		data = bpy.data

		rows = 2
		row = layout.row(align=True)
		row.template_list("NOM_UL_items", "custom_def_list", data, "materials", scn, "custom_index", rows=4)


# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class NOM_PG_IndexMatsArray(PropertyGroup):
	#name = StringProperty() -> Instantiated by default
	arrayIndex = IntProperty(
		name="Index material list",
		default=-1
	)

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
	NOM_OT_ExcludeMat,
	NOM_UL_items,
	NOM_PT_objectList,
	NOM_PG_IndexMatsArray
)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	# Custom scene properties
	bpy.types.Scene.exludeIndexes = CollectionProperty(type=NOM_PG_IndexMatsArray)
	bpy.types.Scene.custom_index = IntProperty()


def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

	del bpy.types.Scene.exludeIndexes
	del bpy.types.Scene.custom_index


if __name__ == "__main__":
	register()