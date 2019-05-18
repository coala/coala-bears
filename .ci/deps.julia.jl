if VERSION < v"0.7.0-DEV.5183"
  Pkg.clone(pwd(), ENV["JL_PKG"])
  Pkg.build(ENV["JL_PKG"])
else
  using Pkg
  Pkg.build()
end
