# Shared updater core: fields read from the manifest

## `min_common` in the manifest (phase 1)

A manifest may carry the optional field `min_common`: the oldest version of the shared contracts repository the project works with (three or four numbers). The updater reads it when it is a version and ignores it when it is anything else (it is never an error, because a manifest that says it must not stop an updater that does not understand it). A misspelled name of the field is still refused as an unknown field. Nothing is decided by the value yet.

The second phase is the publication of the field by the projects, in their manifests and in the shared manifest schema, once every updater of the family reads it.
