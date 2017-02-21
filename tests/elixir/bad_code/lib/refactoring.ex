defmodule Refactoring do
  @moduledoc false
  def some_fun do
    cond do
      false -> 0
      true -> 1
    end
  end
end
