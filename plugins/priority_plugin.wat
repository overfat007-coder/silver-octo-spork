;; WASM text prototype plugin for custom priority scoring.
(module
  (func (export "score") (param i32) (result i32)
    local.get 0
  )
)
