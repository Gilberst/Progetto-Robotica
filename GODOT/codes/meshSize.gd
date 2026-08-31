extends MeshInstance3D
func get_size()->Vector3:
	var lenght=self.mesh.get_aabb().size
	return lenght
